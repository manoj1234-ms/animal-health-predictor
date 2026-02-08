import pandas as pd
import os
import subprocess
import sys

# Constants for validation
REQUIRED_COLUMNS = [
    'Animal', 'Age', 'Gender', 'Breed', 'WBC', 'RBC', 'Hemoglobin', 
    'Platelets', 'Glucose', 'ALT', 'AST', 'Urea', 'Creatinine', 
    'Symptom_Fever', 'Symptom_Lethargy', 'Symptom_Vomiting', 
    'Symptom_Diarrhea', 'Symptom_WeightLoss', 'Symptom_SkinLesion', 
    'Symptom_Coughing', 'Symptom_Lameness', 'Category', 'Disease'
]

CUSTOM_DATA_PATH = 'data/custom_records.csv'
MASTER_DATA_PATH = 'data/enhanced_training_data.csv'

def validate_csv(df):
    """Checks if the uploaded dataframe has all required columns."""
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    return len(missing) == 0, missing

def save_custom_data(df):
    """Appends new data to the custom records file."""
    os.makedirs('data', exist_ok=True)
    if os.path.exists(CUSTOM_DATA_PATH):
        df.to_csv(CUSTOM_DATA_PATH, mode='a', header=False, index=False)
    else:
        df.to_csv(CUSTOM_DATA_PATH, index=False)

def merge_and_retrain():
    """Merges master and custom data, then triggers retraining."""
    if not os.path.exists(CUSTOM_DATA_PATH):
        return False, "No custom data found to merge."

    try:
        df_master = pd.read_csv(MASTER_DATA_PATH)
        df_custom = pd.read_csv(CUSTOM_DATA_PATH)
        
        # Merge
        df_final = pd.concat([df_master, df_custom], ignore_index=True)
        df_final.to_csv(MASTER_DATA_PATH, index=False)
        
        # Trigger retraining
        # We use subprocess to run the training scripts to ensure clean state
        print("🚀 Triggering Stage 1 & 2 Retraining...")
        subprocess.run([sys.executable, 'retrain_models.py'], check=True)
        
        print("🧠 Triggering VetNet (Neural Network) Retraining...")
        subprocess.run([sys.executable, '-m', 'src.train_nn'], check=True)
        
        return True, "Success! System has been retrained with new data."
    except Exception as e:
        return False, f"Retraining failed: {str(e)}"
