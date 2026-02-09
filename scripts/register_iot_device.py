
import requests
import sys
import json

# Configuration
API_URL = "http://localhost:8002/iot/register"

def register_device(device_id, name, species, age, breed, gender):
    """
    Registers a physical IoT device to a specific animal in the VetNet Brain.
    """
    payload = {
        "device_id": device_id,
        "animal_id": f"{species}_{device_id}",
        "species": species,
        "name": name,
        "age": float(age),
        "breed": breed,
        "gender": gender
    }
    
    print(f"📡 Registering Hardware-ID: {device_id}...")
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            print(f"✅ SUCCESS: {name} ({species}) is now live in VetNet Registry.")
            print(f"➡️ Device Response: {response.json()['message']}")
        else:
            print(f"❌ FAILED: API returned {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ CONNECTION ERROR: Ensure simple_api.py is running on port 8002. Detail: {e}")

if __name__ == "__main__":
    # Example usage via command line
    if len(sys.argv) > 1:
        # Expected: python register_device.py TAG_ID NAME SPECIES AGE BREED GENDER
        # Example: python register_device.py TAG_007 Bond Tiger 6 Bengal Male
        register_device(*sys.argv[1:7])
    else:
        print("\n--- VetNet IoT Device Onboarding ---")
        d_id = input("1. Hardware Tag ID (e.g. ESP32_01): ")
        d_name = input("2. Animal Name (e.g. Simba): ")
        d_spec = input("3. Species (e.g. Lion): ")
        d_age = input("4. Age (e.g. 4.5): ")
        d_breed = input("5. Breed (e.g. African): ")
        d_gender = input("6. Gender (Male/Female): ")
        
        register_device(d_id, d_name, d_spec, d_age, d_breed, d_gender)
