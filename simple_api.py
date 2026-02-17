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
import traceback
from datetime import datetime
from fastapi import UploadFile, File, Form
import pypdf
import re
import io


# Try to import from src package
try:
    from src.inference_nn import predict_disease_nn
except ImportError:
    # Try direct import if src is in path or we are in src
    try:
        from inference_nn import predict_disease_nn
    except ImportError as e:
        print(f"ERROR: ML Model Import Error: {e}")
        print("Running in Lightweight Mode (No Neural Network)")
        def predict_disease_nn(data):
            return {"success": False, "error": "ML Model not loaded"}


from src.monitoring import SystemMonitor, start_background_monitoring

app = FastAPI(title="Animal Disease Prediction API (VetNet Powered)")

# Enable CORS for React Frontend
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

monitor = SystemMonitor()

# Import and attach IoT Gateway
from src.iot_gateway import router as iot_router
app.include_router(iot_router, prefix="/iot", tags=["IoT Telemetry"])

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
    try:
        from src.iot_gateway import initialize_dummy_data, start_iot_simulator
        initialize_dummy_data()
        start_iot_simulator(interval=3) # Update every 3 seconds for better real-time feel
    except Exception as e:

        print(f"Error initializing dummy data: {e}")

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
        traceback.print_exc()
        latency_ms = (time.time() - start_time) * 1000
        # Log error
        monitor.log_prediction(request.dict(), {"success": False, "error": str(e)}, latency_ms)
        monitor.log_prediction(request.dict(), {"success": False, "error": str(e)}, latency_ms)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-report")
async def upload_report(file: UploadFile = File(...)):
    """Upload PDF report and extract medical data"""
    try:
        contents = await file.read()
        pdf_file = io.BytesIO(contents)
        reader = pypdf.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        # Simple extraction logic (can be improved with LLM)
        data = {
            "Animal": "Dog",  # Default
            "Age": 5.0,
            "Gender": "Male",
            "WBC": 8.0,
            "RBC": 6.0,
            "Hemoglobin": 14.0,
            "Platelets": 300.0,
            "Glucose": 100.0,
            "Symptom_Fever": 0,
            "Symptom_Lethargy": 0,
            "Symptom_Vomiting": 0
        }

        # Regex Extraction
        if re.search(r"Species:?\s*(\w+)", text, re.IGNORECASE):
            data["Animal"] = re.search(r"Species:?\s*(\w+)", text, re.IGNORECASE).group(1)
        if re.search(r"Age:?\s*(\d*\.?\d+)", text, re.IGNORECASE):
            data["Age"] = float(re.search(r"Age:?\s*(\d*\.?\d+)", text, re.IGNORECASE).group(1))
        if re.search(r"Gender:?\s*(\w+)", text, re.IGNORECASE):
            data["Gender"] = re.search(r"Gender:?\s*(\w+)", text, re.IGNORECASE).group(1)
        
        # Blood values
        if re.search(r"WBC:?\s*(\d*\.?\d+)", text, re.IGNORECASE):
            data["WBC"] = float(re.search(r"WBC:?\s*(\d*\.?\d+)", text, re.IGNORECASE).group(1))
        
        # Symptoms check (keywords)
        if "fever" in text.lower(): data["Symptom_Fever"] = 1
        if "lethargy" in text.lower(): data["Symptom_Lethargy"] = 1
        if "vomiting" in text.lower(): data["Symptom_Vomiting"] = 1

        return {
            "success": True, 
            "extracted_data": data,
            "raw_text_preview": text[:500] + "..."
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"PDF Processing Failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Start server
    print("Starting API server on port 8002...")
    uvicorn.run("simple_api:app", host="0.0.0.0", port=8002, reload=True)
