"""
Retrain Models with Comprehensive Dataset
Trains models on 8 species, 8 categories, 193 diseases
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
import joblib
import os

print("="*70)
print(" "*20 + "MODEL RETRAINING")
print("="*70)

# Load comprehensive dataset
print("\n📂 Loading enhanced dataset...")
df = pd.read_csv('data/enhanced_training_data.csv')
print(f"✅ Loaded {len(df)} samples")
print(f"📊 Species: {df['Animal'].nunique()}")
print(f"📊 Categories: {df['Category'].nunique()}")
print(f"📊 Diseases: {df['Disease'].nunique()}")

# Prepare features
feature_cols = [col for col in df.columns if col not in ['Category', 'Disease']]
X = df[feature_cols]
y_category = df['Category']
y_disease = df['Disease']

# Encode categories
category_encoder = LabelEncoder()
y_category_encoded = category_encoder.fit_transform(y_category)

print(f"\n🎯 Features: {len(feature_cols)}")
print(f"🎯 Categories: {', '.join(category_encoder.classes_)}")

# Stage 1: Category prediction
print("\n" + "="*70)
print("STAGE 1: TRAINING CATEGORY PREDICTION MODEL")
print("="*70)

numeric_features = ['Age', 'WBC', 'RBC', 'Hemoglobin', 'Platelets', 
                   'Glucose', 'ALT', 'AST', 'Urea', 'Creatinine']
categorical_features = ['Animal', 'Gender', 'Breed']

from sklearn.preprocessing import OneHotEncoder

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ],
    n_jobs=1  # Important for compatibility
)

stage1_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', XGBClassifier(
        n_estimators=200,
        max_depth=8,
        learning_rate=0.1,
        random_state=42,
        n_jobs=1
    ))
])

print("Training Stage 1 model...")
stage1_pipeline.fit(X, y_category_encoded)
print("✅ Stage 1 training complete")

# Stage 2: Disease prediction per category
print("\n" + "="*70)
print("STAGE 2: TRAINING DISEASE-SPECIFIC MODELS")
print("="*70)

stage2_models = {}
disease_encoders = {}

for category in df['Category'].unique():
    print(f"\n📊 Training model for {category}...")
    mask = df['Category'] == category
    X_cat = X[mask]
    y_cat = y_disease[mask]
    
    # Create disease encoder for this category
    disease_encoder = LabelEncoder()
    y_cat_encoded = disease_encoder.fit_transform(y_cat)
    
    # Create pipeline for this category
    stage2_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', XGBClassifier(
            n_estimators=200,
            max_depth=8,
            learning_rate=0.1,
            random_state=42,
            n_jobs=1
        ))
    ])
    
    stage2_pipeline.fit(X_cat, y_cat_encoded)
    
    stage2_models[category] = stage2_pipeline
    disease_encoders[category] = disease_encoder
    
    print(f"   ✅ Trained on {len(X_cat)} samples, {len(disease_encoder.classes_)} diseases")
    print(f"   Diseases: {', '.join(disease_encoder.classes_[:3])}...")

# Save models
print("\n" + "="*70)
print("SAVING MODELS")
print("="*70)

os.makedirs('models', exist_ok=True)

joblib.dump(stage1_pipeline, 'models/stage1_pipeline.pkl')
joblib.dump(stage2_models, 'models/stage2_models.pkl')
joblib.dump(category_encoder, 'models/category_encoder.pkl')
joblib.dump(disease_encoders, 'models/disease_encoders.pkl')

print("\n✅ All models saved successfully!")
print(f"   📁 models/stage1_pipeline.pkl")
print(f"   📁 models/stage2_models.pkl (8 category models)")
print(f"   📁 models/category_encoder.pkl")
print(f"   📁 models/disease_encoders.pkl (8 disease encoders)")

# Summary
print("\n" + "="*70)
print("TRAINING SUMMARY")
print("="*70)
print(f"\n🎯 Stage 1: Category prediction")
print(f"   - Categories: {len(category_encoder.classes_)}")
print(f"   - Features: {len(feature_cols)}")
print(f"\n🎯 Stage 2: Disease prediction")
print(f"   - Category-specific models: {len(stage2_models)}")
print(f"   - Total unique diseases: {df['Disease'].nunique()}")
print(f"\n🐾 Species Coverage:")
for animal in sorted(df['Animal'].unique()):
    count = len(df[df['Animal'] == animal])
    print(f"   - {animal}: {count} samples")

print("\n✅ RETRAINING COMPLETE!")
print("="*70 + "\n")
