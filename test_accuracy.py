"""
Quick accuracy test for 20-species model
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import sys
import os

sys.path.insert(0, 'src')
from src.model_compatibility import apply_global_patches
apply_global_patches()

print("="*70)
print(" "*20 + "20-SPECIES MODEL ACCURACY TEST")
print("="*70)

# Load data
df = pd.read_csv('data/training_data.csv')
print(f"\n✅ Loaded {len(df)} samples")
print(f"   Species: {df['Animal'].nunique()}")
print(f"   Categories: {df['Category'].nunique()}")
print(f"   Diseases: {df['Disease'].nunique()}")

# Prepare data
feature_cols = [col for col in df.columns if col not in ['Category', 'Disease']]
X = df[feature_cols]
y_category = df['Category']
y_disease = df['Disease']

# Split
X_train, X_test, y_cat_train, y_cat_test, y_dis_train, y_dis_test = train_test_split(
    X, y_category, y_disease, test_size=0.3, random_state=42, stratify=y_category
)

print(f"\n📊 Test split: {len(X_test)} samples")

# Load models
stage1_pipeline = joblib.load('models/stage1_pipeline.pkl')
category_encoder = joblib.load('models/category_encoder.pkl')
stage2_models = joblib.load('models/stage2_models.pkl')
disease_encoders = joblib.load('models/disease_encoders.pkl')

print("\n🤖 Models loaded")

# Test Stage 1
y_cat_pred = stage1_pipeline.predict(X_test)
y_cat_pred_names = category_encoder.inverse_transform(y_cat_pred)
stage1_accuracy = accuracy_score(y_cat_test, y_cat_pred_names)

print(f"\n🎯 STAGE 1 (Category) Accuracy: {stage1_accuracy:.2%}")

# Test Stage 2
correct_stage2 = 0
total_stage2 = 0

for i in range(len(X_test)):
    true_category = y_cat_test.iloc[i]
    true_disease = y_dis_test.iloc[i]
    
    if true_category in stage2_models:
        model = stage2_models[true_category]
        encoder = disease_encoders[true_category]
        
        X_sample = X_test.iloc[[i]]
        pred_encoded = model.predict(X_sample)[0]
        pred_disease = encoder.inverse_transform([pred_encoded])[0]
        
        if pred_disease == true_disease:
            correct_stage2 += 1
        total_stage2 += 1

stage2_accuracy = correct_stage2 / total_stage2 if total_stage2 > 0 else 0

print(f"🎯 STAGE 2 (Disease) Accuracy: {stage2_accuracy:.2%}")

# Overall
print(f"\n📈 OVERALL COMBINED Accuracy: {(stage1_accuracy * stage2_accuracy):.2%}")

print(f"\n✅ Correctly predicted: {int(correct_stage2)} out of {total_stage2} diseases")

# Species breakdown
print(f"\n🐾 SPECIES COVERAGE:")
for species in sorted(df['Animal'].unique()):
    count = len(df[df['Animal'] == species])
    print(f"   {species}: {count} samples")

print("\n" + "="*70)
print("TEST COMPLETE!")
print("="*70 + "\n")
