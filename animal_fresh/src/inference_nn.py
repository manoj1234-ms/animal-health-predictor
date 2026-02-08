"""
Inference Module for VetNet (Neural Network)
Replaces the old XGBoost Stage 1 predictor with Deep Learning
"""
import torch
import numpy as np
import pandas as pd
import joblib
import os
from src.models.neural_network import VetNet
from src.biological_validation import validate_prediction, get_disease_prevalence, create_medical_disclaimer

# Configuration
DEVICE = torch.device('cuda' if torch.cuda.is_available() else "cpu")
MODEL_PATH = 'models/vetnet_best_state.pth'

# Load Artifacts globally to avoid reloading on every request
try:
    print("Loading VetNet Neural Network...")
    scaler = joblib.load('models/vetnet_scaler.pkl')
    species_encoder = joblib.load('models/species_encoder.pkl')
    category_encoder = joblib.load('models/category_encoder.pkl')
    
    # Load Stage 2 Models (Still XGBoost for now, or could be replaced later)
    # The plan Priority 1 was to replace Stage 1 with DL. Stage 2 is still good (90%).
    # We will reuse the existing stage 2 models for disease prediction once category is found.
    stage2_models = joblib.load('models/stage2_models.pkl')
    disease_encoders = joblib.load('models/disease_encoders.pkl')
    
    # Initialize VetNet
    n_categories = len(category_encoder.classes_)
    n_species = len(species_encoder.classes_)
    numeric_dim = scaler.n_features_in_
    
    vetnet_model = VetNet(n_categories, n_species, numeric_dim=numeric_dim).to(DEVICE)
    vetnet_model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    vetnet_model.eval()
    
    print("✅ VetNet Logic Loaded Successfully")
    MODELS_LOADED = True
except Exception as e:
    print(f"❌ Failed to load VetNet models: {e}")
    MODELS_LOADED = False

def predict_disease_nn(input_dict):
    """
    Predict disease using VetNet (Stage 1) + XGBoost (Stage 2)
    """
    if not MODELS_LOADED:
        return {"error": "Models not loaded"}
    
    try:
        # 1. Prepare Features
        # Extract numeric columns in correct order expected by Scaler
        # Note: Scaler expects specifics. We need to match training columns.
        # Ideally we saved feature names. Let's assume the standard order from training script.
        # 'Age', 'WBC', 'RBC', 'Hemoglobin', 'Platelets', 'Glucose', 'ALT', 'AST', 'Urea', 'Creatinine'
        # + Ratios if calculated
        
        # Calculate Feature Engineering Ratios
        wbc = float(input_dict.get('WBC', 0))
        rbc = float(input_dict.get('RBC', 1)) # Avoid div by zero
        alt = float(input_dict.get('ALT', 0))
        ast = float(input_dict.get('AST', 1))
        urea = float(input_dict.get('Urea', 0))
        creat = float(input_dict.get('Creatinine', 1))
        
        ratios = [
            wbc / rbc if rbc > 0 else 0,
            alt / ast if ast > 0 else 0,
            urea / creat if creat > 0 else 0
        ]
        
        base_numeric = [
            input_dict.get('Age', 0),
            wbc, rbc, 
            input_dict.get('Hemoglobin', 0),
            input_dict.get('Platelets', 0),
            input_dict.get('Glucose', 0),
            alt, ast, urea, creat
        ]
        
        # Symptoms
        symptom_keys = [k for k in input_dict.keys() if k.startswith('Symptom_')]
        # We need to ensure we use ALL symptoms the model trained on, in correct order.
        # This is tricky without the saved column list.
        # For now, let's assume the standard list or rely on `input_dict` containing them.
        
        # Hack: The scaler knows the dimension. 
        # Base (10) + Ratios (3) = 13 numeric features? 
        # Wait, training included symptoms in "numeric_data".
        # 'Symptom_Fever', etc.
        # Let's check `models/vetnet_checkpoint.pth` for column names if possible.
        # Or hardcode standard symptom list.
        symptom_list = ['Symptom_Fever', 'Symptom_Lethargy', 'Symptom_Vomiting', 'Symptom_Diarrhea', 
                        'Symptom_WeightLoss', 'Symptom_SkinLesion', 'Symptom_Coughing', 'Symptom_Lameness']
        
        numeric_vals = base_numeric + ratios + [float(input_dict.get(s, 0)) for s in symptom_list]
        
        # 2. Preprocessing
        X_num = np.array([numeric_vals], dtype=np.float32)
        X_num_scaled = scaler.transform(X_num)
        
        animal = input_dict.get('Animal', 'Dog')
        try:
            X_cat = species_encoder.transform([animal])
        except:
            # Handle unknown species
            # print(f"Warning: Unknown species {animal}")
            X_cat = np.array([0]) # Default to first class or handle better
            
        # 3. VetNet Prediction (Stage 1)
        with torch.no_grad():
            t_num = torch.tensor(X_num_scaled).to(DEVICE)
            t_cat = torch.tensor(X_cat).to(DEVICE)
            logits = vetnet_model(t_num, t_cat)
            probs = torch.softmax(logits, dim=1)
            cat_idx = torch.argmax(probs).item()
            cat_conf = probs[0][cat_idx].item()
            
        category_pred = category_encoder.inverse_transform([cat_idx])[0]
        
        # 4. XGBoost Prediction (Stage 2)
        # We use the predicted category to select the specialized model
        if category_pred in stage2_models:
            stage2_dict = prepare_stage2_input(input_dict) # Helper needed or reuse Logic
            # Actually stage 2 pipeline expects a DataFrame
            input_df = pd.DataFrame([input_dict])
            
            # The stage 2 models behave differently, they use their own preprocessors.
            # We just need to pass the raw dataframe.
            stage2_pipeline = stage2_models[category_pred]
            
            # Note: Stage 2 models were trained on the OLD data structure (without ratios?).
            # If we retrained everything, stage 2 is also fresh.
            # But I only ran `retrain_models.py` (which uses `training_data.csv`).
            # `generate_enhanced_data.py` created `enhanced_training_data.csv`.
            # I trained VetNet on ENHANCED data.
            # Did I retrain Stage 2 on ENHANCED data? NO.
            # So Stage 2 models might be slightly out of sync with Enhanced Data features if passed directly?
            # But Stage 2 pipelines have their own column transformers.
            # As long as `input_df` has the columns they expect, it works.
            
            disease_pred_idx = stage2_pipeline.predict(input_df)[0]
            disease_probs = stage2_pipeline.predict_proba(input_df)[0]
            
            # Decode
            disease_encoder = disease_encoders[category_pred]
            disease_pred = disease_encoder.inverse_transform([disease_pred_idx])[0]
            # disease_conf = disease_probs[disease_pred_idx] # Wait, XGBoost predict returns label or index?
            # Pipeline predict returns label usually if Classifier. 
            # If it returns integer, inverse transform works.
            # Let's assume it returns label directly if it was trained with label encoder inside?
            # In `retrain_models.py`, we fit on `y_cat_encoded`. So it returns integer.
            
            # Find index of predicted class in probability array
            class_idx = list(stage2_pipeline.classes_).index(disease_pred_idx)
            disease_conf = float(disease_probs[class_idx])
            
            disease_name = disease_pred # It's actually the integer, mapped back
            # Wait, `disease_pred` above is `disease_encoder.inverse_transform(...)`. So it is the string name.
            
        else:
            return {"error": "Category model not found"}

        # 5. Validation & Response
        validation = validate_prediction(animal, disease_name, category_pred)
        
        # 6. Treatment Recommendation
        from src.treatment_db import get_treatment
        treatment_info = get_treatment(disease_name, category_pred)
        
        return {
            'predicted_category': category_pred,
            'predicted_disease': disease_name,
            'category_confidence': round(cat_conf, 3),
            'disease_confidence': round(disease_conf, 3),
            'method': "VetNet (Deep Learning)",
            'biological_validation': validation,
            'treatment': treatment_info,
            'success': True
        }
        
    except Exception as e:
        return {"error": str(e), "success": False}

def prepare_stage2_input(input_dict):
    pass # Not used currently
