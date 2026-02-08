"""
Evaluate Neural Network Model (VetNet)
Uses best_state.pth + separate joblib pickles to avoid unpickling errors
"""
import torch
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
import joblib
from src.models.neural_network import VetNet
import os

DEVICE = torch.device('cuda' if torch.cuda.is_available() else "cpu")

def evaluate_vetnet():
    print("\n" + "="*60)
    print("EVALUATING VETNET (PYTORCH)")
    print("="*60)
    
    # 1. Load Artifacts
    if not os.path.exists('models/vetnet_best_state.pth'):
        print("❌ Model best state not found.")
        return
        
    try:
        # Load sklearn objects
        scaler = joblib.load('models/vetnet_scaler.pkl')
        species_encoder = joblib.load('models/species_encoder.pkl')
        category_encoder = joblib.load('models/category_encoder.pkl')
    except Exception as e:
        print(f"❌ Failed to load sklearn objects: {e}")
        return

    # Load Model State
    n_categories = len(category_encoder.classes_)
    n_species = len(species_encoder.classes_)
    # Determine numeric dim from scaler
    numeric_dim = scaler.n_features_in_
    
    model = VetNet(
        n_categories=n_categories,
        n_species=n_species,
        numeric_dim=numeric_dim
    ).to(DEVICE)
    
    model.load_state_dict(torch.load('models/vetnet_best_state.pth', map_location=DEVICE))
    model.eval()
    
    # 2. Load Data for Evaluation
    data_path = 'data/enhanced_training_data.csv'
    df = pd.read_csv(data_path)
    print(f"✅ Loaded {len(df)} samples for evaluation")
    
    # Prepare inputs (Reconstruct logic from training)
    numeric_cols = ['Age', 'WBC', 'RBC', 'Hemoglobin', 'Platelets', 'Glucose', 'ALT', 'AST', 'Urea', 'Creatinine']
    extra_cols = ['WBC_RBC_Ratio', 'ALT_AST_Ratio', 'Urea_Creat_Ratio']
    for col in extra_cols:
        if col in df.columns:
            numeric_cols.append(col)
            
    symptom_cols = [c for c in df.columns if c.startswith('Symptom_')]
    
    numeric_data = df[numeric_cols + symptom_cols].values
    species_encoded = species_encoder.transform(df['Animal'])
    y_encoded = category_encoder.transform(df['Category'])
    
    # Train/Test Split (Same random state as training)
    # We only care about X_test and y_test
    _, X_num_test, _, X_cat_test, _, y_test = train_test_split(
        numeric_data, species_encoded, y_encoded, test_size=0.2, stratify=y_encoded, random_state=42
    )
    
    # Scale Numeric
    X_num_test_scaled = scaler.transform(X_num_test)
    
    # 3. Inference
    print("🚀 Running Inference on Test Set...")
    batch_size = 32
    predictions = []
    
    with torch.no_grad():
        for i in range(0, len(X_num_test_scaled), batch_size):
            batch_num = X_num_test_scaled[i:i+batch_size]
            batch_cat = X_cat_test[i:i+batch_size]
            
            t_num = torch.tensor(batch_num, dtype=torch.float32).to(DEVICE)
            t_cat = torch.tensor(batch_cat, dtype=torch.long).to(DEVICE)
            
            logits = model(t_num, t_cat)
            _, preds = torch.max(logits, 1)
            predictions.extend(preds.cpu().numpy())
            
    y_pred = np.array(predictions)
    
    # 4. Metrics
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n✅ Test Accuracy: {accuracy:.2%}")
    
    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=category_encoder.classes_))
    
    # Save Report
    with open('models/vetnet_evaluation_report.txt', 'w') as f:
        f.write(f"Test Accuracy: {accuracy:.2%}\n\n")
        f.write(classification_report(y_test, y_pred, target_names=category_encoder.classes_))
    print("Check models/vetnet_evaluation_report.txt for details.")

if __name__ == "__main__":
    evaluate_vetnet()
