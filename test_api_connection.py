import requests
import json

# Define the API endpoint
url = "http://localhost:8000/predict"

# Mimic the payload sent by the "Patient Intake" form
payload = {
    "Animal": "Dog",
    "Age": 4.0,
    "Gender": "Male", # API requires this, even if form defaults it
    "Breed": "Labrador",
    "WBC": 12.5,
    "RBC": 6.8,
    "Hemoglobin": 15.0,
    "Platelets": 320.0,
    "Glucose": 95.0,
    "ALT": 42.0,
    "AST": 38.0,
    "Urea": 22.0,
    "Creatinine": 1.2,
    "Symptom_Fever": 0,
    "Symptom_Lethargy": 1,
    "Symptom_Vomiting": 1,
    "Symptom_Diarrhea": 0,
    "Symptom_WeightLoss": 0,
    "Symptom_SkinLesion": 0,
    "Symptom_Coughing": 0,
    "Symptom_Lameness": 0
}

print(f"Sending request to {url}...")
try:
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"\n❌ Connection Failed: {e}")
