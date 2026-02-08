"""
Train Neural Network Model (VetNet - PyTorch Version)
Uses Enhanced Dataset and PyTorch
"""
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from src.models.neural_network import VetNet
import joblib
import os

print(f"CUDA Available: {torch.cuda.is_available()}")
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using Device: {DEVICE}")

# Dataset Class
class VetDataset(Dataset):
    def __init__(self, X_num, X_cat, y=None):
        self.X_num = torch.tensor(X_num, dtype=torch.float32)
        self.X_cat = torch.tensor(X_cat, dtype=torch.long)
        self.y = torch.tensor(y, dtype=torch.long) if y is not None else None
        
    def __len__(self):
        return len(self.X_num)
    
    def __getitem__(self, idx):
        if self.y is not None:
            return self.X_num[idx], self.X_cat[idx], self.y[idx]
        return self.X_num[idx], self.X_cat[idx]

def train_vetnet():
    print("\n" + "="*60)
    print("TRAINING VETNET (PYTORCH)")
    print("="*60)
    
    # 1. Load Enhanced Data
    data_path = 'data/enhanced_training_data.csv'
    if not os.path.exists(data_path):
        print("❌ Enhanced data not found. Run generate_enhanced_data.py first.")
        return
        
    df = pd.read_csv(data_path)
    print(f"✅ Loaded {len(df)} samples from {data_path}")
    
    # 2. Features & Labels
    numeric_cols = ['Age', 'WBC', 'RBC', 'Hemoglobin', 'Platelets', 'Glucose', 'ALT', 'AST', 'Urea', 'Creatinine']
    # Add Feature Engineering columns if they exist
    extra_cols = ['WBC_RBC_Ratio', 'ALT_AST_Ratio', 'Urea_Creat_Ratio']
    for col in extra_cols:
        if col in df.columns:
            numeric_cols.append(col)
            
    symptom_cols = [c for c in df.columns if c.startswith('Symptom_')]
    
    # Concatenate numeric and symptoms for numeric input branch
    numeric_data = df[numeric_cols + symptom_cols].values
    
    # Categorical Inputs (Species)
    species_encoder = LabelEncoder()
    species_encoded = species_encoder.fit_transform(df['Animal'])
    
    # Labels (Category)
    category_encoder = LabelEncoder()
    y_encoded = category_encoder.fit_transform(df['Category'])
    
    # Dimensions
    num_categories = len(category_encoder.classes_)
    num_species = len(species_encoder.classes_)
    num_features = numeric_data.shape[1]
    
    print(f"📊 Input Features: {num_features}")
    print(f"📊 Categories: {num_categories}")
    print(f"📊 Species: {num_species}")
    
    # 3. Train/Test Split
    X_num_train, X_num_test, X_cat_train, X_cat_test, y_train, y_test = train_test_split(
        numeric_data, species_encoded, y_encoded, test_size=0.2, stratify=y_encoded, random_state=42
    )
    
    # 4. Scaling
    scaler = StandardScaler()
    X_num_train_scaled = scaler.fit_transform(X_num_train)
    X_num_test_scaled = scaler.transform(X_num_test)
    
    # 5. DataLoaders
    train_dataset = VetDataset(X_num_train_scaled, X_cat_train, y_train)
    test_dataset = VetDataset(X_num_test_scaled, X_cat_test, y_test)
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    
    # 6. Initialize Model
    model = VetNet(
        n_categories=num_categories,
        n_species=num_species,
        numeric_dim=num_features
    ).to(DEVICE)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    # 7. Training Loop
    print("\n🚀 Starting Training...")
    epochs = 50
    best_acc = 0.0
    
    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        correct = 0
        total = 0
        
        for X_num, X_cat, y in train_loader:
            X_num, X_cat, y = X_num.to(DEVICE), X_cat.to(DEVICE), y.to(DEVICE)
            
            optimizer.zero_grad()
            outputs = model(X_num, X_cat)
            loss = criterion(outputs, y)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += y.size(0)
            correct += (predicted == y).sum().item()
        
        train_acc = 100 * correct / total
        
        # Validation
        model.eval()
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for X_num, X_cat, y in test_loader:
                X_num, X_cat, y = X_num.to(DEVICE), X_cat.to(DEVICE), y.to(DEVICE)
                outputs = model(X_num, X_cat)
                _, predicted = torch.max(outputs.data, 1)
                val_total += y.size(0)
                val_correct += (predicted == y).sum().item()
        
        val_acc = 100 * val_correct / val_total
        
        if (epoch+1) % 5 == 0:
            print(f"Epoch [{epoch+1}/{epochs}] Loss: {train_loss/len(train_loader):.4f} Train Acc: {train_acc:.2f}% Val Acc: {val_acc:.2f}%")
            
        if val_acc > best_acc:
            best_acc = val_acc
            # Save Best Model State
            torch.save(model.state_dict(), 'models/vetnet_best_state.pth')
    
    # 8. Final Evaluation
    print(f"\n✅ Best Validation Accuracy: {best_acc:.2f}%")
    
    # 9. Save Artifacts for Inference
    os.makedirs('models', exist_ok=True)
    
    # Save Full Checkpoint
    checkpoint = {
        'model_state_dict': model.state_dict(), # Or load best
        'scaler': scaler,
        'species_encoder': species_encoder,
        'category_encoder': category_encoder,
        'n_categories': num_categories,
        'n_species': num_species,
        'numeric_dim': num_features,
        'numeric_cols': numeric_cols,
        'symptom_cols': symptom_cols
    }
    torch.save(checkpoint, 'models/vetnet_checkpoint.pth')
    
    # Also save separate sklearn objects for compatibility with other scripts if needed
    joblib.dump(scaler, 'models/vetnet_scaler.pkl')
    joblib.dump(species_encoder, 'models/species_encoder.pkl')
    joblib.dump(category_encoder, 'models/category_encoder.pkl')
    
    print("✅ Model Checkpoint saved to models/vetnet_checkpoint.pth")

if __name__ == "__main__":
    train_vetnet()
