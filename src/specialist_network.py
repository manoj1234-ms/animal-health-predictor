"""
Specialist Network & Clinic Database
Stores information about veterinary clinics, their specialties, and coordinates.
Loads data from clinics.json database.
"""
import json
import os

# Base directory for finding the data folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "clinics.json")

def load_clinic_db():
    """Load clinics from the database file."""
    try:
        # Create data directory if it doesn't exist (failsafe)
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        if not os.path.exists(DB_PATH):
            return []
            
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Database Error: {e}")
        return []

# Dynamic database loading
CLINIC_DB = load_clinic_db()

DISEASE_TO_SPECIALTY = {
    "Infectious": ["Emergency Medicine", "Internal Medicine"],
    "Neurological": ["Neurology", "Internal Medicine"],
    "Dermatological": ["Dermatology"],
    "Gastrointestinal": ["Internal Medicine", "General Surgery"],
    "Respiratory": ["Internal Medicine", "Cardiology"],
    "Cardiovascular": ["Cardiology", "Heart Surgery"],
    "Orthopedic": ["Surgery", "Imaging"],
    "General": ["General Surgery", "Vaccinations"]
}

def get_specialists_for_disease(category):
    """
    AI Logic to find best specialists based on disease category.
    """
    needed_specialties = DISEASE_TO_SPECIALTY.get(category, ["Internal Medicine"])
    
    recommended = []
    for clinic in CLINIC_DB:
        # Check if any clinic specialty matches the needed specialties
        if any(s in needed_specialties for s in clinic["specialties"]):
            recommended.append(clinic)
            
    return sorted(recommended, key=lambda x: x['rating'], reverse=True)

def find_emergency_clinics():
    """Return all 24/7 emergency centers."""
    return [c for c in CLINIC_DB if c.get("emergency", False)]

def reload_db():
    """Manually refresh the clinic data."""
    global CLINIC_DB
    CLINIC_DB = load_clinic_db()
