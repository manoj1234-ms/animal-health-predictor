"""
Neural Network Model for Animal Disease Prediction (PyTorch)
Input: Numeric features + Species Embedding
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import joblib
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.preprocessing import StandardScaler

class VetNet(nn.Module):
    def __init__(self, n_categories=8, n_species=20, n_breeds=3, numeric_dim=21):
        super(VetNet, self).__init__()
        
        # Hyperparameters
        self.numeric_dim = numeric_dim
        self.embedding_dim = 8
        self.n_species = n_species + 1 # +1 for unknown
        
        # 1. Numeric Branch
        self.fc_num1 = nn.Linear(numeric_dim, 128)
        self.bn_num1 = nn.BatchNorm1d(128)
        self.dropout1 = nn.Dropout(0.3)
        
        # 2. Categorical Branch (Species)
        self.species_embed = nn.Embedding(self.n_species, self.embedding_dim)
        
        # 3. Fusion & Deep Layers
        # Input to deep layers = 128 (numeric) + 8 (species) = 136
        self.fc1 = nn.Linear(128 + self.embedding_dim, 256)
        self.bn1 = nn.BatchNorm1d(256)
        self.dropout2 = nn.Dropout(0.3)
        
        self.fc2 = nn.Linear(256, 128)
        self.bn2 = nn.BatchNorm1d(128)
        self.dropout3 = nn.Dropout(0.3)
        
        # Output
        self.output = nn.Linear(128, n_categories)
        
    def forward(self, x_num, x_cat):
        # Numeric Path
        x_n = F.relu(self.bn_num1(self.fc_num1(x_num)))
        x_n = self.dropout1(x_n)
        
        # Categorical Path
        x_c = self.species_embed(x_cat).view(-1, self.embedding_dim) # Flatten
        
        # Concatenate
        x = torch.cat((x_n, x_c), dim=1)
        
        # Deep Layers
        x = F.relu(self.bn1(self.fc1(x)))
        x = self.dropout2(x)
        
        x = F.relu(self.bn2(self.fc2(x)))
        x = self.dropout3(x)
        
        # Output (Logits)
        out = self.output(x)
        return out

class VetNetClassifier(BaseEstimator, ClassifierMixin):
    """
    Sklearn-compatible wrapper for VetNet PyTorch model
    """
    def __init__(self, n_categories=8, n_species=20, numeric_dim=10, 
                 lr=0.001, epochs=50, batch_size=32, device=None):
        self.n_categories = n_categories
        self.n_species = n_species
        self.numeric_dim = numeric_dim
        self.lr = lr
        self.epochs = epochs
        self.batch_size = batch_size
        self.device = device if device else ('cuda' if torch.cuda.is_available() else 'cpu')
        
        self.model = None
        self.optimizer = None
        self.criterion = nn.CrossEntropyLoss()
        self.scaler = StandardScaler()
        
    def fit(self, X_num, X_cat, y):
        self.model = VetNet(
            n_categories=self.n_categories,
            n_species=self.n_species,
            numeric_dim=X_num.shape[1]
        ).to(self.device)
        
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)
        
        # Scale numeric data
        X_num_scaled = self.scaler.fit_transform(X_num)
        
        # Convert to Tensor
        dataset = torch.utils.data.TensorDataset(
            torch.tensor(X_num_scaled, dtype=torch.float32),
            torch.tensor(X_cat, dtype=torch.long),
            torch.tensor(y, dtype=torch.long)
        )
        loader = torch.utils.data.DataLoader(dataset, batch_size=self.batch_size, shuffle=True)
        
        # Training Loop
        self.model.train()
        for epoch in range(self.epochs):
            total_loss = 0
            correct = 0
            total = 0
            
            for xb_num, xb_cat, yb in loader:
                xb_num, xb_cat, yb = xb_num.to(self.device), xb_cat.to(self.device), yb.to(self.device)
                
                self.optimizer.zero_grad()
                logits = self.model(xb_num, xb_cat)
                loss = self.criterion(logits, yb)
                loss.backward()
                self.optimizer.step()
                
                total_loss += loss.item()
                _, predicted = torch.max(logits.data, 1)
                total += yb.size(0)
                correct += (predicted == yb).sum().item()
            
            acc = 100 * correct / total
            if (epoch+1) % 10 == 0:
                print(f"Epoch [{epoch+1}/{self.epochs}], Loss: {total_loss/len(loader):.4f}, Acc: {acc:.2f}%")
                
        return self

    def predict(self, X_num, X_cat):
        self.model.eval()
        X_num_scaled = self.scaler.transform(X_num)
        
        with torch.no_grad():
            t_num = torch.tensor(X_num_scaled, dtype=torch.float32).to(self.device)
            t_cat = torch.tensor(X_cat, dtype=torch.long).to(self.device)
            logits = self.model(t_num, t_cat)
            _, predicted = torch.max(logits, 1)
            
        return predicted.cpu().numpy()

    def predict_proba(self, X_num, X_cat):
        self.model.eval()
        X_num_scaled = self.scaler.transform(X_num)
        
        with torch.no_grad():
            t_num = torch.tensor(X_num_scaled, dtype=torch.float32).to(self.device)
            t_cat = torch.tensor(X_cat, dtype=torch.long).to(self.device)
            logits = self.model(t_num, t_cat)
            probs = F.softmax(logits, dim=1)
            
        return probs.cpu().numpy()
    
    def save(self, path='models/vetnet.pth'):
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'scaler': self.scaler,
            'n_categories': self.n_categories,
            'n_species': self.n_species,
            'numeric_dim': self.numeric_dim
        }, path)
        print(f"Saved model to {path}")

def load_vetnet(path='models/vetnet.pth'):
    checkpoint = torch.load(path)
    model = VetNet(
        n_categories=checkpoint['n_categories'],
        n_species=checkpoint['n_species'],
        numeric_dim=checkpoint['numeric_dim']
    )
    model.load_state_dict(checkpoint['model_state_dict'])
    wrapper = VetNetClassifier(
        n_categories=checkpoint['n_categories'], 
        n_species=checkpoint['n_species'],
        numeric_dim=checkpoint['numeric_dim']
    )
    wrapper.model = model
    wrapper.scaler = checkpoint['scaler']
    wrapper.model.eval()
    return wrapper
