from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import time
import random
from datetime import datetime, timedelta
import threading
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
    # Zoo Animals
    "TAG_101": {"animal_id": "Lion_Alpha", "species": "Lion", "name": "Simba", "age": 4.5, "breed": "African", "gender": "Male"},
    "TAG_102": {"animal_id": "Elephant_01", "species": "Elephant", "name": "Hathi", "age": 12.0, "breed": "African", "gender": "Female"},
    
    # Farm Animals - Cattle
    "TAG_201": {"animal_id": "Cow_Bassie", "species": "Cattle", "name": "Bessie", "age": 3.0, "breed": "Holstein", "gender": "Female"},
    "TAG_202": {"animal_id": "Cow_Daisy", "species": "Cattle", "name": "Daisy", "age": 2.5, "breed": "Jersey", "gender": "Female"},
    "TAG_203": {"animal_id": "Bull_Ferdinand", "species": "Cattle", "name": "Ferdinand", "age": 4.0, "breed": "Angus", "gender": "Male"},

    # Horses
    "TAG_301": {"animal_id": "Horse_Spirit", "species": "Horse", "name": "Spirit", "age": 5.0, "breed": "Mustang", "gender": "Male"},
    "TAG_302": {"animal_id": "Horse_Rain", "species": "Horse", "name": "Rain", "age": 4.0, "breed": "Paint", "gender": "Female"},

    # Pigs
    "TAG_401": {"animal_id": "Pig_Wilbur", "species": "Pig", "name": "Wilbur", "age": 1.0, "breed": "Yorkshire", "gender": "Male"},
    "TAG_402": {"animal_id": "Pig_Babe", "species": "Pig", "name": "Babe", "age": 0.8, "breed": "Berkshire", "gender": "Male"},
    
    # Sheep & Goats
    "TAG_501": {"animal_id": "Sheep_Dolly", "species": "Sheep", "name": "Dolly", "age": 2.0, "breed": "Merino", "gender": "Female"},
    "TAG_502": {"animal_id": "Goat_Billy", "species": "Goat", "name": "Billy", "age": 3.0, "breed": "Alpine", "gender": "Male"},

    # Poultry
    "TAG_601": {"animal_id": "Chicken_Little", "species": "Chicken", "name": "Little", "age": 0.5, "breed": "Leghorn", "gender": "Female"},
    "TAG_602": {"animal_id": "Chicken_Big", "species": "Chicken", "name": "Big Red", "age": 1.0, "breed": "Rhode Island", "gender": "Male"},

    # Pets
    "TAG_701": {"animal_id": "Dog_Buddy", "species": "Dog", "name": "Buddy", "age": 3.0, "breed": "Golden Retriever", "gender": "Male"},
    "TAG_702": {"animal_id": "Dog_Max", "species": "Dog", "name": "Max", "age": 5.0, "breed": "German Shepherd", "gender": "Male"},
}

# Helper to Initialize Dummy Data
def initialize_dummy_data():
    """Populates the device_stream_buffer with initial dummy data for all registered devices."""
    print(f"Adding dummy data for {len(device_registry)} devices...")
    current_time = time.time()
    
    for device_id, info in device_registry.items():
        # Baseline vitals per species
        base_temp = 38.0
        base_hr = 70.0
        
        if info['species'] == 'Cattle': base_temp, base_hr = 38.5, 60
        elif info['species'] == 'Horse': base_temp, base_hr = 37.5, 40
        elif info['species'] == 'Pig': base_temp, base_hr = 39.0, 75
        elif info['species'] == 'Sheep': base_temp, base_hr = 39.0, 75
        elif info['species'] == 'Goat': base_temp, base_hr = 39.0, 80
        elif info['species'] == 'Chicken': base_temp, base_hr = 41.5, 275
        elif info['species'] == 'Dog': base_temp, base_hr = 38.5, 90
        elif info['species'] == 'Lion': base_temp, base_hr = 38.0, 50
        elif info['species'] == 'Elephant': base_temp, base_hr = 36.5, 30

        # Create 5-10 history points
        history = []
        for i in range(10):
            t_offset = (10 - i) * 60 # 10 minutes history
            
            # Randomized fluctuations
            temp = base_temp + random.uniform(-0.5, 0.5)
            hr = base_hr + random.uniform(-5, 5)
            activity = random.uniform(20, 100)
            battery = 100 - (i * 0.1)

            # Introduce some anomalies (Dummy Critical/Warning states)
            if device_id == "TAG_203": # Sick Bull (FMD?)
                temp += 2.0 # Fever
                hr += 20
                activity = 5 # Lethargic
            elif device_id == "TAG_601": # Sick Chicken (Flu?)
                temp += 1.5
                hr += 10
                activity = 10
            elif device_id == "TAG_402": # Heat stress Pig
                temp += 1.0
                hr += 15

            data = TelemetryData(
                device_id=device_id,
                animal_id=info['animal_id'],
                species=info['species'],
                timestamp=current_time - t_offset,
                temperature=round(temp, 1),
                heart_rate=round(hr, 0),
                activity_level=round(activity, 1),
                battery_level=round(battery, 1)
            )
            history.append(data)
        
        device_stream_buffer[device_id] = history
    
    print("Dummy data initialization complete.")

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

# Background Simulator Logic
def start_iot_simulator(interval=5):
    """
    Starts a background thread that periodically appends new telemetry data 
    for all registered devices to simulate real-time behavior.
    """
    def simulation_loop():
        print(f"🚀 IoT Simulator started (Interval: {interval}s)")
        while True:
            current_time = time.time()
            for device_id, info in device_registry.items():
                if device_id not in device_stream_buffer:
                    device_stream_buffer[device_id] = []
                
                # Get last reading as baseline
                if device_stream_buffer[device_id]:
                    last = device_stream_buffer[device_id][-1]
                    base_temp = last.temperature
                    base_hr = last.heart_rate
                    base_battery = last.battery_level
                else:
                    # Generic defaults if no history
                    base_temp, base_hr, base_battery = 38.0, 70.0, 100.0

                # Subtle fluctuations
                temp = base_temp + random.uniform(-0.2, 0.2)
                hr = base_hr + random.uniform(-2, 2)
                activity = random.uniform(10, 80)
                battery = max(0, base_battery - 0.01)

                # Persist anomalies for specific tags as defined in initialize_dummy_data
                if device_id == "TAG_203": # Sick Bull
                    temp = max(temp, 40.5) + random.uniform(-0.1, 0.1)
                    hr = max(hr, 80) + random.uniform(-1, 1)
                    activity = random.uniform(2, 8)
                elif device_id == "TAG_601": # Sick Chicken
                    temp = max(temp, 42.5) + random.uniform(-0.1, 0.1)
                    hr = max(hr, 285) + random.uniform(-1, 1)

                new_data = TelemetryData(
                    device_id=device_id,
                    animal_id=info['animal_id'],
                    species=info['species'],
                    timestamp=current_time,
                    temperature=round(temp, 1),
                    heart_rate=round(hr, 0),
                    activity_level=round(activity, 1),
                    battery_level=round(battery, 1)
                )

                device_stream_buffer[device_id].append(new_data)
                
                # Keep last 50 readings
                if len(device_stream_buffer[device_id]) > 50:
                    device_stream_buffer[device_id].pop(0)

            time.sleep(interval)

    thread = threading.Thread(target=simulation_loop, daemon=True)
    thread.start()
    return thread


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
