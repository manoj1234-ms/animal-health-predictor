
import sys
import os
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, accuracy_score
from tqdm import tqdm

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.inference_nn import predict_disease_nn

def evaluate_system():
    print("="*70)
    print("VETNET SYSTEM ACCURACY EVALUATION")
    print("="*70)
    
    # 1. Load Data
    data_path = 'data/enhanced_training_data.csv'
    if not os.path.exists(data_path):
        print(f"ERROR: Data file {data_path} not found.")
        return
        
    df = pd.read_csv(data_path)
    print(f"INFO: Loaded {len(df)} samples")
    
    # Take a representative sample for evaluation (e.g., 20% or 500 samples for speed)
    sample_size = min(500, len(df))
    eval_df = df.sample(sample_size, random_state=42)
    print(f"TESTING: Evaluating on {sample_size} random samples...")
    
    y_cat_true = []
    y_cat_pred = []
    y_dis_true = []
    y_dis_pred = []
    
    errors = []
    
    # 2. Run Predictions
    for idx, row in tqdm(eval_df.iterrows(), total=sample_size):
        input_data = row.to_dict()
        
        # Ground Truth
        true_category = str(row['Category'])
        true_disease = str(row['Disease'])
        
        try:
            result = predict_disease_nn(input_data)
            
            if result.get('success'):
                pred_category = result.get('predicted_category')
                pred_disease = result.get('predicted_disease')
                
                y_cat_true.append(true_category)
                y_cat_pred.append(pred_category)
                y_dis_true.append(true_disease)
                y_dis_pred.append(pred_disease)
            else:
                errors.append(f"Prediction failed for index {idx}: {result.get('error')}")
        except Exception as e:
            errors.append(f"Crash for index {idx}: {str(e)}")

    # 3. Present Results
    print("\n" + "="*70)
    print("EVALUATION RESULTS")
    print("="*70)
    
    if len(y_cat_true) > 0:
        cat_acc = accuracy_score(y_cat_true, y_cat_pred)
        dis_acc = accuracy_score(y_dis_true, y_dis_pred)
        
        print(f"\nRESULT: Stage 1 (Category) Accuracy: {cat_acc:.2%}")
        print(f"RESULT: Stage 2 (Disease) Accuracy: {dis_acc:.2%}")

        
        print("\nSUMMARY: Category Classification Report:")
        print(classification_report(y_cat_true, y_cat_pred, zero_division=0))
        
        # Check for discrepancies
        print("\nERROR ANALYSIS: First 5 disease mismatches:")
        mismatches = 0
        for i in range(len(y_dis_true)):
            if y_dis_true[i] != y_dis_pred[i]:
                print(f"  - Actual: {y_dis_true[i]} | Predicted: {y_dis_pred[i]} (Cat: {y_cat_pred[i]})")
                mismatches += 1
                if mismatches >= 5:
                    break
    else:
        print("ERROR: No valid predictions were made.")
        
    if errors:
        print(f"\nWARNING: Encountered {len(errors)} execution errors.")
        for err in errors[:5]:
            print(f"  - {err}")

if __name__ == "__main__":
    evaluate_system()
