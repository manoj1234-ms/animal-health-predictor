"""
Inference engine for animal disease prediction.
Uses the compatibility layer for Python 3.13 support.
Includes biological validation.
"""

import pandas as pd
import numpy as np
from src.model_compatibility import load_compatible_models, suppress_sklearn_warnings
from src.biological_validation import (
    validate_prediction,
    get_disease_prevalence,
    get_alternative_diseases,
    create_medical_disclaimer
)

# Suppress warnings
suppress_sklearn_warnings()

# Load models globally
try:
    print("Loading models with compatibility fixes...")
    stage1_pipeline, stage2_models, category_encoder, disease_encoders = load_compatible_models()
    print("✅ Models loaded successfully")
    MODELS_LOADED = True
except Exception as e:
    print(f"❌ Failed to load models: {e}")
    MODELS_LOADED = False

def predict_disease(input_dict):
    """
    Predict disease from input features with biological validation.
    
    Args:
        input_dict: Dictionary with patient features
        
    Returns:
        Dictionary with prediction results and validation
    """
    if not MODELS_LOADED:
        return {
            "error": "Models not loaded",
            "message": "System not ready"
        }
    
    try:
        # Convert to DataFrame
        input_df = pd.DataFrame([input_dict])
        animal = input_dict.get('Animal', 'Unknown')
        
        # Stage 1: Predict category
        category_pred = stage1_pipeline.predict(input_df)[0]
        category_proba = stage1_pipeline.predict_proba(input_df)[0]
        category_name = category_encoder.inverse_transform([category_pred])[0]
        category_confidence = float(category_proba[category_pred])
        
        # Stage 2: Predict disease
        stage2_model = stage2_models[category_name]
        disease_pred = stage2_model.predict(input_df)[0]
        disease_proba = stage2_model.predict_proba(input_df)[0]
        disease_name = disease_encoders[category_name].inverse_transform([disease_pred])[0]
        disease_confidence = float(disease_proba[disease_pred])
        
        # Biological validation
        validation = validate_prediction(animal, disease_name, category_name)
        
        # Get disease prevalence info
        prevalence = get_disease_prevalence(animal, disease_name)
        
        # Get alternatives if not biologically plausible
        alternatives = []
        if not validation['is_biologically_plausible']:
            alternatives = get_alternative_diseases(animal, category_name, top_n=3)
        
        return {
            'predicted_category': category_name,
            'predicted_disease': disease_name,
            'category_confidence': round(category_confidence, 3),
            'disease_confidence': round(disease_confidence, 3),
            'animal': animal,
            'biological_validation': validation,
            'disease_prevalence': prevalence,
            'alternative_diseases': alternatives,
            'medical_disclaimer': create_medical_disclaimer(),
            'prediction_safe': validation['is_biologically_plausible'] and disease_confidence > 0.5,
            'success': True
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "message": "Prediction failed",
            "success": False
        }
