"""
Model Evaluation and Accuracy Testing
Generates confusion matrix, classification reports, and accuracy metrics
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    classification_report, 
    confusion_matrix, 
    accuracy_score,
    precision_recall_fscore_support,
    roc_auc_score
)
from sklearn.model_selection import train_test_split
import joblib
import os
import sys

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from model_compatibility import load_compatible_models, suppress_sklearn_warnings
from biological_validation import validate_prediction

suppress_sklearn_warnings()

def load_test_data():
    """Load or create test data for evaluation"""
    data_path = 'data/training_data.csv'
    
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        print(f"Loaded {len(df)} samples from {data_path}")
    else:
        print("No training data found. Please run src/train.py first.")
        return None
    
    return df

def evaluate_stage1_model(pipeline, X_test, y_test, category_encoder):
    """Evaluate Stage 1 (Category Prediction) model"""
    print("\n" + "="*60)
    print("STAGE 1: CATEGORY PREDICTION EVALUATION")
    print("="*60)
    
    # Make predictions
    y_pred = pipeline.predict(X_test)
    y_pred_proba = pipeline.predict_proba(X_test)
    
    # Get category names
    category_names = category_encoder.classes_
    
    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n✅ Overall Accuracy: {accuracy:.2%}")
    
    # Classification Report
    print("\n📊 Classification Report:")
    print(classification_report(
        y_test, 
        y_pred, 
        target_names=category_names,
        digits=3
    ))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\n🔢 Confusion Matrix:")
    print("Predicted →")
    print(f"Actual ↓    {' '.join([f'{c:>12}' for c in category_names])}")
    for i, actual_cat in enumerate(category_names):
        print(f"{actual_cat:>12}  {' '.join([f'{cm[i][j]:>12}' for j in range(len(category_names))])}")
    
    # Per-class metrics
    precision, recall, f1, support = precision_recall_fscore_support(
        y_test, y_pred, average=None, labels=range(len(category_names))
    )
    
    print("\n📈 Per-Category Metrics:")
    print(f"{'Category':<15} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support':<10}")
    print("-" * 65)
    for i, cat in enumerate(category_names):
        print(f"{cat:<15} {precision[i]:<12.3f} {recall[i]:<12.3f} {f1[i]:<12.3f} {support[i]:<10.0f}")
    
    return {
        'accuracy': accuracy,
        'confusion_matrix': cm,
        'classification_report': classification_report(y_test, y_pred, target_names=category_names, output_dict=True),
        'category_names': category_names
    }

def evaluate_stage2_models(stage2_models, disease_encoders, X_test, y_test, category_test):
    """Evaluate Stage 2 (Disease Prediction) models"""
    print("\n" + "="*60)
    print("STAGE 2: DISEASE PREDICTION EVALUATION")
    print("="*60)
    
    results = {}
    
    for category in stage2_models.keys():
        print(f"\n{'─'*60}")
        print(f"Evaluating {category} Model")
        print(f"{'─'*60}")
        
        # Get samples for this category
        category_mask = category_test == category
        
        if category_mask.sum() == 0:
            print(f"⚠️ No test samples for {category}")
            continue
        
        X_cat = X_test[category_mask]
        y_cat_raw = y_test[category_mask]
        
        # Encode disease labels for this category
        disease_encoder = disease_encoders[category]
        try:
            y_cat = disease_encoder.transform(y_cat_raw)
        except:
            print(f"⚠️ Error encoding labels for {category}")
            continue
        
        # Make predictions
        model = stage2_models[category]
        y_pred = model.predict(X_cat)
        
        # Get disease names
        disease_names = disease_encoder.classes_
        
        # Accuracy
        accuracy = accuracy_score(y_cat, y_pred)
        print(f"✅ Accuracy: {accuracy:.2%}")
        
        # Classification Report
        print(f"\n📊 Classification Report:")
        print(classification_report(
            y_cat,
            y_pred,
            target_names=disease_names,
            digits=3,
            zero_division=0
        ))
        
        # Confusion Matrix
        cm = confusion_matrix(y_cat, y_pred)
        print(f"\n🔢 Confusion Matrix:")
        print("Predicted →")
        print(f"Actual ↓    {' '.join([f'{d:>15}' for d in disease_names])}")
        for i, actual_dis in enumerate(disease_names):
            print(f"{actual_dis:>15}  {' '.join([f'{cm[i][j]:>15}' for j in range(len(disease_names))])}")
        
        results[category] = {
            'accuracy': accuracy,
            'confusion_matrix': cm,
            'disease_names': disease_names,
            'num_samples': len(y_cat)
        }
    
    return results

def test_biological_validation(df):
    """Test biological validation on sample data"""
    print("\n" + "="*60)
    print("BIOLOGICAL VALIDATION TEST")
    print("="*60)
    
    validation_results = []
    
    # Test a sample of predictions
    sample_size = min(20, len(df))
    sample_df = df.sample(sample_size, random_state=42)
    
    print(f"\nTesting {sample_size} random samples...")
    print("\n{'Animal':<10} {'Disease':<20} {'Category':<15} {'Valid':<10} {'Reason'}")
    print("-" * 80)
    
    for _, row in sample_df.iterrows():
        animal = row['Animal']
        disease = row['Disease']
        category = row['Category']
        
        validation = validate_prediction(animal, disease, category)
        
        is_valid = validation['is_biologically_plausible']
        reason = validation['validation_reason'][:30]
        
        validation_results.append(validation)
        
        status = "✅" if is_valid else "❌"
        print(f"{animal:<10} {disease:<20} {category:<15} {status:<10} {reason}")
    
    # Summary
    valid_count = sum(1 for v in validation_results if v['is_biologically_plausible'])
    print(f"\n📊 Validation Summary:")
    print(f"  Valid Predictions: {valid_count}/{sample_size} ({valid_count/sample_size:.1%})")
    print(f"  Invalid Predictions: {sample_size-valid_count}/{sample_size} ({(sample_size-valid_count)/sample_size:.1%})")
    
    return validation_results

def run_full_evaluation():
    """Run complete model evaluation"""
    print("\n" + "="*70)
    print(" "*20 + "MODEL EVALUATION REPORT")
    print("="*70)
    
    # Load data
    print("\n📂 Loading Data...")
    df = load_test_data()
    
    if df is None:
        print("❌ Cannot proceed without data")
        return
    
    # Prepare data
    feature_cols = [col for col in df.columns if col not in ['Category', 'Disease']]
    X = df[feature_cols]
    y_category = df['Category']
    y_disease = df['Disease']
    
    # Split data
    X_train, X_test, y_cat_train, y_cat_test, y_dis_train, y_dis_test = train_test_split(
        X, y_category, y_disease, test_size=0.3, random_state=42, stratify=y_category
    )
    
    print(f"📊 Data Split:")
    print(f"  Training samples: {len(X_train)}")
    print(f"  Testing samples: {len(X_test)}")
    
    # Load models
    print("\n🤖 Loading Models...")
    stage1_pipeline, stage2_models, category_encoder, disease_encoders = load_compatible_models()
    
    print(f"DEBUG: Encoder classes: {category_encoder.classes_}")
    
    # Encode labels safely (handling unseen labels if any, though stratified split minimizes this)
    # Filter known classes only
    known_mask = y_cat_test.isin(category_encoder.classes_)
    if (~known_mask).any():
        print(f"⚠️ Dropped {(~known_mask).sum()} samples with unknown categories")
        X_test = X_test[known_mask]
        y_cat_test = y_cat_test[known_mask]
        y_dis_test = y_dis_test[known_mask]
    
    y_cat_test_encoded = category_encoder.transform(y_cat_test)
    
    # Evaluate Stage 1
    stage1_results = evaluate_stage1_model(
        stage1_pipeline, X_test, y_cat_test_encoded, category_encoder
    )
    
    # Evaluate Stage 2
    stage2_results = evaluate_stage2_models(
        stage2_models, disease_encoders, X_test, y_dis_test, y_cat_test
    )
    
    # Test biological validation
    validation_results = test_biological_validation(df)
    
    # Overall Summary
    print("\n" + "="*70)
    print(" "*25 + "FINAL SUMMARY")
    print("="*70)
    
    print(f"\n🎯 Stage 1 (Category) Accuracy: {stage1_results['accuracy']:.2%}")
    
    stage2_avg_accuracy = np.mean([r['accuracy'] for r in stage2_results.values()])
    print(f"🎯 Stage 2 (Disease) Average Accuracy: {stage2_avg_accuracy:.2%}")
    
    valid_count = sum(1 for v in validation_results if v['is_biologically_plausible'])
    print(f"🎯 Biological Validation Rate: {valid_count/len(validation_results):.1%}")
    
    print("\n✅ Evaluation Complete!")
    print("\n" + "="*70 + "\n")
    
    return {
        'stage1': stage1_results,
        'stage2': stage2_results,
        'validation': validation_results
    }

if __name__ == "__main__":
    results = run_full_evaluation()
