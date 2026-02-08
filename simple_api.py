"""
FastAPI application for animal disease prediction.
Updated to use Neural Network (VetNet) and Real-Time Monitoring.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os
import time
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.inference_nn import predict_disease_nn
from src.monitoring import SystemMonitor, start_background_monitoring

app = FastAPI(title="Animal Disease Prediction API (VetNet Powered)")
monitor = SystemMonitor()

class PredictionRequest(BaseModel):
    Animal: str
    Country: Optional[str] = "Global"
    State: Optional[str] = "Unknown"
    City: Optional[str] = "Unknown"
    Age: float
    Gender: str
    Breed: Optional[str] = "Mixed"
    WBC: Optional[float] = 8.0
    RBC: Optional[float] = 6.0
    Hemoglobin: Optional[float] = 14.0
    Platelets: Optional[float] = 300.0
    Glucose: Optional[float] = 100.0
    ALT: Optional[float] = 40.0
    AST: Optional[float] = 40.0
    Urea: Optional[float] = 25.0
    Creatinine: Optional[float] = 1.0
    Symptom_Fever: Optional[int] = 0
    Symptom_Lethargy: Optional[int] = 0
    Symptom_Vomiting: Optional[int] = 0
    Symptom_Diarrhea: Optional[int] = 0
    Symptom_WeightLoss: Optional[int] = 0
    Symptom_SkinLesion: Optional[int] = 0
    Symptom_Coughing: Optional[int] = 0
    Symptom_Lameness: Optional[int] = 0

@app.on_event("startup")
def startup_event():
    """Start background tasks"""
    start_background_monitoring(interval=10) # Log system health every 10s

@app.get("/")
def read_root():
    return {
        "message": "Animal Disease Prediction API (VetNet)",
        "version": "3.0",
        "model": "Deep Learning (PyTorch)",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/predict")
def predict(request: PredictionRequest):
    """Make a disease prediction using VetNet"""
    start_time = time.time()
    try:
        input_dict = request.dict()
        
        # Use new Neural Network Inference
        result = predict_disease_nn(input_dict)
        
        # Calculate latency
        latency_ms = (time.time() - start_time) * 1000
        
        # Log to monitoring system
        monitor.log_prediction(input_dict, result, latency_ms)
        
        if not result.get('success', False):
            raise HTTPException(status_code=500, detail=result.get('error', 'Prediction failed'))
        
        return result
    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        # Log error
        monitor.log_prediction(request.dict(), {"success": False, "error": str(e)}, latency_ms)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Start server
    print("Starting API server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
