# Animal Disease Prediction System

## Python 3.13 Compatible Edition

This is a complete rewrite of the animal disease prediction system with full Python 3.13 compatibility.

### Features
- ✅ Two-stage ML prediction (Category → Disease)
- ✅ Python 3.13 compatible
- ✅ scikit-learn version compatibility layer
- ✅ XGBoost compatibility fixes
- ✅ FastAPI REST API
- ✅ Docker support
- ✅ CI/CD with GitHub Actions

### Quick Start

#### 1. Setup Environment
```bash
python -m venv animal_env
source animal_env/bin/activate  # On Windows: animal_env\Scripts\activate
pip install -r requirements.txt
```

#### 2. Train Models
```bash
python src/train.py
```

#### 3. Run API
```bash
python simple_api.py
```

Visit http://localhost:8000/docs for API documentation

#### 4. Make a Prediction
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Animal": "Dog",
    "Age": 5.0,
    "Gender": "Male",
    "Breed": "Labrador"
  }'
```

### Docker Deployment

```bash
docker build -t animal-disease-predictor .
docker run -p 8000:8000 animal-disease-predictor
```

### Project Structure
```
animal_fresh/
├── src/
│   ├── train.py                 # Training script
│   ├── inference.py             # Prediction engine
│   └── model_compatibility.py   # Python 3.13 compatibility layer
├── models/                      # Trained models (generated)
├── data/                        # Training data
├── .github/workflows/           # CI/CD pipelines
├── simple_api.py                # FastAPI application
├── Dockerfile                   # Docker configuration
└── requirements.txt             # Dependencies
```

### CI/CD

The project includes GitHub Actions workflows that:
- Test on Python 3.11, 3.12, and 3.13
- Train models automatically
- Run inference tests
- Build and push Docker images

### License
MIT License
