
import time
import random
import requests
import json
import sys

# Configuration
API_URL = "http://localhost:8002/iot/telemetry"
SPECIES_LIST = ['Cattle', 'Buffalo', 'Dog', 'Horse', 'Sheep', 'Lion', 'Elephant', 'Tiger', 'Pig', 'Goat', 'Chicken', 'Rabbit', 'Parrot', 'Lizard', 'Snake', 'Turtle', 'Fish']
NUM_DEVICES = 30

def generate_telemetry(device_id, species):
    """Generate realistic vital signs based on species"""
    
    # Baselines (approximate)
    baselines = {
        'Cattle': {'temp': 38.6, 'hr': 60, 'act': 50},
        'Dog': {'temp': 38.9, 'hr': 90, 'act': 80},
        'Cat': {'temp': 38.5, 'hr': 120, 'act': 70},
        'Horse': {'temp': 37.8, 'hr': 35, 'act': 40},
        'Sheep': {'temp': 39.0, 'hr': 75, 'act': 60},
        'Buffalo': {'temp': 38.2, 'hr': 55, 'act': 45},
        'Lion': {'temp': 38.5, 'hr': 45, 'act': 60},
        'Tiger': {'temp': 38.0, 'hr': 50, 'act': 55},
        'Elephant': {'temp': 36.5, 'hr': 30, 'act': 30},
        'Pig': {'temp': 39.2, 'hr': 70, 'act': 50},
        'Goat': {'temp': 39.1, 'hr': 80, 'act': 65},
        'Chicken': {'temp': 41.5, 'hr': 250, 'act': 90},
        'Rabbit': {'temp': 39.4, 'hr': 200, 'act': 85},
        'Lizard': {'temp': 28.0, 'hr': 40, 'act': 20},
        'Snake': {'temp': 25.0, 'hr': 30, 'act': 10},
        'Turtle': {'temp': 26.0, 'hr': 25, 'act': 15},
        'Fish': {'temp': 22.0, 'hr': 60, 'act': 40}
    }
    
    base = baselines.get(species, baselines['Cattle'])
    
    # Add random noise (Normal variations)
    temp = round(base['temp'] + random.uniform(-0.5, 0.5), 1)
    hr = int(base['hr'] + random.uniform(-5, 10))
    act = int(base['act'] + random.uniform(-20, 30))
    
    # 10% Chance of Abnormal Event (Simulation)
    if random.random() < 0.10:
        event_type = random.choice(['fever', 'stress', 'lethargy'])
        if event_type == 'fever':
            temp += 2.0 # Spike temperature
        elif event_type == 'stress':
            hr += 40 # Spike heart rate
        elif event_type == 'lethargy':
            act = 5 # Drop activity
            
    return {
        "device_id": device_id,
        "animal_id": f"{species}_{device_id.split('_')[1]}",
        "species": species,
        "timestamp": time.time(),
        "temperature": temp,
        "heart_rate": hr,
        "activity_level": float(act),
        "battery_level": round(random.uniform(20.0, 100.0), 1)
    }

def main():
    print(f"🚀 Starting IoT Simulation for {NUM_DEVICES} devices...")
    print(f"📡 Sending data to: {API_URL}")
    
    devices = []
    for i in range(NUM_DEVICES):
        spec = random.choice(SPECIES_LIST)
        devices.append({"id": f"TAG_{i+100}", "species": spec})
        
    print(f"📋 Device Registry: {json.dumps(devices, indent=2)}")
    
    try:
        while True:
            for dev in devices:
                payload = generate_telemetry(dev['id'], dev['species'])
                
                try:
                    resp = requests.post(API_URL, json=payload)
                    
                    # Print status
                    status_icon = "Aa"
                    if resp.status_code == 200:
                        data = resp.json()
                        if data['status'] == 'CRITICAL':
                            status_icon = "QC CRITICAL ABNORMALITY"
                            print(f"⚠️ {status_icon} | {payload['animal_id']} | Temp: {payload['temperature']} | HR: {payload['heart_rate']} | {data['actions']}")
                        elif data['status'] == 'WARNING':
                            status_icon = "⚠️ WARNING"
                            print(f"{status_icon} | {payload['animal_id']} | {data['actions']}")
                        else:
                            # print(".", end="", flush=True) # Quiet mode for normal
                            pass
                    else:
                        print(f"❌ Error: {resp.status_code}")
                        
                except Exception as e:
                    print(f"Connection Error: {e}")
                    
            time.sleep(2) # Send batch every 2 seconds
            
            # Newline for visual cleanliness
            # print("") 
            
    except KeyboardInterrupt:
        print("\n🛑 Simulation stopped.")

if __name__ == "__main__":
    main()
