
import sys
import os
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.inference_nn import predict_disease_nn

test_input = {
    "Animal": "Lion",
    "Age": 5.0,
    "WBC": 10.0,
    "RBC": 6.0,
    "Hemoglobin": 14.0,
    "Platelets": 300.0,
    "Glucose": 100.0,
    "ALT": 40.0,
    "AST": 40.0,
    "Urea": 30.0,
    "Creatinine": 1.0,
    "Symptom_Fever": 1,
    "Symptom_Lethargy": 1,
    "Symptom_Vomiting": 0,
    "Symptom_Diarrhea": 0,
    "Symptom_WeightLoss": 0,
    "Symptom_SkinLesion": 0,
    "Symptom_Coughing": 0,
    "Symptom_Lameness": 0,
    "Symptom_NasalDischarge": 1,
    "Symptom_EyeDischarge": 1,
    "Symptom_Drooling": 0,
    "Symptom_Blisters": 0
}

try:
    print("Testing prediction function...")
    result = predict_disease_nn(test_input)
    print("Prediction Result:")
    print(result)
except Exception as e:
    import traceback
    traceback.print_exc()
