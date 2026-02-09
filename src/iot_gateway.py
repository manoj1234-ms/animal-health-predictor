from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import time
from .biological_rules import analyze_vitals

router = APIRouter()

# Data Models
class TelemetryData(BaseModel):
    device_id: str
    animal_id: str
    species: str
    timestamp: float
    temperature: Optional[float] = None
    heart_rate: Optional[float] = None
    activity_level: Optional[float] = None
    battery_level: Optional[float] = 100.0

class AlertResponse(BaseModel):
    status: str
    alerts: List[dict]
    actions: List[str]

# In-memory registry for device-to-animal mapping
# Format: { device_id: { "animal_id": str, "species": str, "name": str, "age": float, "breed": str, "gender": str } }
device_registry = {
    # Pre-populate with some demo devices
    "TAG_101": {"animal_id": "Lion_Alpha", "species": "Lion", "name": "Simba", "age": 4.5, "breed": "African", "gender": "Male"},
    "TAG_102": {"animal_id": "Elephant_01", "species": "Elephant", "name": "Hathi", "age": 12.0, "breed": "African", "gender": "Female"}
}

# In-memory store for demo purposes (In prod, use Redis/DB)
# Format: { device_id: [TelemetryData, ...] }
device_stream_buffer = {}

class DeviceRegistration(BaseModel):
    device_id: str
    animal_id: str
    species: str
    name: str
    age: float
    breed: str
    gender: str

@router.post("/register")
async def register_device(reg: DeviceRegistration):
    """Register a physical device to an animal profile"""
    device_registry[reg.device_id] = reg.dict()
    # Initialize buffer if not exists
    if reg.device_id not in device_stream_buffer:
        device_stream_buffer[reg.device_id] = []
    return {"status": "success", "message": f"Device {reg.device_id} registered to {reg.name}"}

@router.post("/telemetry", response_model=AlertResponse)
async def ingest_telemetry(data: TelemetryData):
    """
    Ingest real-time telemetry from IoT Collars/Tags.
    """
    # 1. Store Data (Simulated persistence)
    if data.device_id not in device_stream_buffer:
        device_stream_buffer[data.device_id] = []
    
    # Keep last 50 readings
    device_stream_buffer[data.device_id].append(data)
    if len(device_stream_buffer[data.device_id]) > 50:
        device_stream_buffer[data.device_id].pop(0)

    # 2. Analyze Vitals immediately (Edge Computing Pattern)
    analysis = analyze_vitals(
        animal_type=data.species,
        temp=data.temperature,
        hr=data.heart_rate
    )

    # 3. Formulate Response/Actions
    actions = []
    status = "NORMAL"

    if analysis['alerts']:
        status = "ALERT"
        # Simple logical rules for actions
        for alert in analysis['alerts']:
            if alert['severity'] == 'CRITICAL':
                status = "CRITICAL"
                actions.append(f"IMMEDIATE ATTENTION: Check {data.animal_id} for {alert['param']}")
            elif alert['severity'] == 'WARNING':
                actions.append(f"Monitor: {data.animal_id} showing signs of {alert['param']} stress")

    # 4. Check Activity Levels (Simple logic)
    if data.activity_level is not None:
        # Example: Cow with very low activity -> Lethargy/Illness
        if data.species == 'Cattle' and data.activity_level < 10.0:
            status = "WARNING" if status == "NORMAL" else status
            analysis['alerts'].append({
                'severity': 'WARNING',
                'message': 'Low Activity: Possible lethargy or lameness',
                'param': 'Activity'
            })
            actions.append("Check for lameness or isolate animal")

    return {
        "status": status,
        "alerts": analysis['alerts'],
        "actions": list(set(actions))
    }

@router.get("/device/{device_id}/history")
async def get_device_history(device_id: str):
    """Retrieve history for a specific device"""
    if device_id not in device_stream_buffer:
        return {"history": []}
    return {"history": device_stream_buffer[device_id]}

@router.get("/dashboard/summary")
async def get_dashboard_summary():
    """
    Get a summary of all active devices and their current status.
    Ideal for the main dashboard view.
    """
    summary = []
    current_time = time.time()
    
    for device_id, history in device_stream_buffer.items():
        if not history:
            continue
            
        last_reading = history[-1]
        
        # Analyze vitals (re-run logic to ensure we have latest status)
        analysis = analyze_vitals(
            animal_type=last_reading.species,
            temp=last_reading.temperature,
            hr=last_reading.heart_rate
        )
        
        status = "HEALTHY"
        # Determine overall status
        for alert in analysis['alerts']:
            if alert['severity'] == 'CRITICAL':
                status = "CRITICAL"
                break
            elif alert['severity'] == 'WARNING' and status != "CRITICAL":
                status = "WARNING"
        
        summary.append({
            "device_id": device_id,
            "animal_id": last_reading.animal_id,
            "species": last_reading.species,
            "last_seen": last_reading.timestamp,
            "seconds_ago": int(current_time - last_reading.timestamp),
            "status": status,
            "temperature": last_reading.temperature,
            "heart_rate": last_reading.heart_rate,
            "activity": last_reading.activity_level,
            "battery": last_reading.battery_level,
            "alerts": [a['message'] for a in analysis['alerts']]
        })
        
    return {"devices": summary, "count": len(summary)}

@router.post("/diagnose/{device_id}")
async def diagnose_device_telemetry(device_id: str):
    """
    Run the full AI Disease Prediction Model on the latest telemetry data for a device.
    """
    if device_id not in device_stream_buffer or not device_stream_buffer[device_id]:
        raise HTTPException(status_code=404, detail="Device not found or no data")

    # Get latest reading
    reading = device_stream_buffer[device_id][-1]
    
    # Map Telemetry -> AI Input Features
    # Note: We infer symptoms based on vital signs for the AI
    
    # 1. Detect Fever
    # (Simple logic: if temp > threshold, Symptom_Fever = 1)
    analysis = analyze_vitals(reading.species, temp=reading.temperature, hr=reading.heart_rate)
    has_fever = 0
    has_stress = 0 # Maps to Lethargy or Pain
    
    for alert in analysis['alerts']:
        if "Fever" in alert['message']:
            has_fever = 1
        if "Tachycardia" in alert['message']: # High HR
            has_stress = 1
            
    # 2. Detect Lethargy (Low Activity)
    is_lethargic = 0
    if reading.activity_level is not None and reading.activity_level < 20: 
        is_lethargic = 1
    
    # Detect overall status for symptom mapping
    current_status = "HEALTHY"
    for alert in analysis['alerts']:
        if alert['severity'] == 'CRITICAL':
            current_status = "CRITICAL"
            break
        elif alert['severity'] == 'WARNING' and current_status != "CRITICAL":
            current_status = "WARNING"

    # 3. New 'Real Data' Symptoms (Simulated for Demo based on vitals)
    has_nasal_discharge = 0
    has_eye_discharge = 0
    has_drooling = 0
    has_blisters = 0
    
    if has_fever:
        # High correlation with respiratory symptoms
        if reading.species in ['Cattle', 'Pig', 'Dog']:
            has_nasal_discharge = 1 if time.time() % 2 > 1 else 0 # Deterministic-ish simulation
            has_eye_discharge = 1 if time.time() % 3 > 2 else 0
            
    if current_status == 'CRITICAL' and reading.species in ['Cattle', 'Pig']:
        # Characteristic of Foot & Mouth Disease (FMD) logic
        has_drooling = 1
        has_blisters = 1 
        
    # 4. Lookup Registry Data for AI Context
    reg_info = device_registry.get(device_id, {})
    
    # Construct AI feature vector
    ai_input = {
        "Animal": reading.species,
        "Age": reg_info.get("age", 5.0), # Use registry or default
        "Temperature": reading.temperature, 
        "HeartRate": reading.heart_rate,
        "Symptom_Fever": has_fever,
        "Symptom_Lethargy": is_lethargic,
        "Symptom_Vomiting": 0,
        "Symptom_Diarrhea": 0,
        "Symptom_WeightLoss": 0,
        "Symptom_SkinLesion": 0,
        "Symptom_Coughing": 0,
        "Symptom_Lameness": 1 if current_status == 'CRITICAL' else 0,
        "Symptom_NasalDischarge": has_nasal_discharge,
        "Symptom_EyeDischarge": has_eye_discharge,
        "Symptom_Drooling": has_drooling,
        "Symptom_Blisters": has_blisters,
        # Default demographics/location
        "Country": "Global",
        "State": "Unknown",
        "City": "Unknown",
        "Breed": reg_info.get("breed", "Mixed"),
        "Gender": reg_info.get("gender", "Male"),
        # Default blood work (since we don't have sensors for this yet)
        "WBC": 10.0,
        "RBC": 6.0,
        "Hemoglobin": 14.0, 
        "Platelets": 300.0,
        "Glucose": 100.0,
        "ALT": 40.0,
        "AST": 40.0,
        "Urea": 30.0,
        "Creatinine": 1.0
    }
    
    # Dynamic Import to avoid circular deps and allow safe failure
    try:
        from inference_nn import predict_disease_nn
        result = predict_disease_nn(ai_input)
    except Exception as e:
        import traceback
        print(f"❌ AI Diagnosis Error for {device_id}: {e}")
        traceback.print_exc()
        # Fallback for lightweight mode or failure
        result = {
            "predicted_disease": "Inconclusive Analysis",
            "confidence": 0.0,
            "severity": "Unknown",
            "success": False,
            "error": str(e),
            "treatment": {"treatment_plan": "Recalibrate sensors and retry diagnosis."}
        }
        
    return {
        "device_id": device_id,
        "timestamp": time.time(),
        "ai_diagnosis": result
    }
