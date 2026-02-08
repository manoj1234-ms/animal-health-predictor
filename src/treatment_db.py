"""
Veterinary Treatment Database
Contains recommended treatments, medications, and follow-up care for common animal diseases.
"""
import json
import os

TREATMENT_DB = {
    # Viral
    "Canine Parvovirus": {
        "treatment_plan": "Immediate hospitalization required. IV fluid therapy for dehydration is critical.",
        "medications": ["Maropitant (antiemetic)", "Broad-spectrum antibiotics (to prevent secondary infection)", "Pain management"],
        "follow_up": "Check white blood cell count daily. Isolate from other dogs for 2 weeks.",
        "prognosis": "Good with early aggressive treatment (80-90% survival)."
    },
    "Feline Panleukopenia": {
        "treatment_plan": "Intensive supportive care. Isolation is mandatory.",
        "medications": ["IV Fluids (Lactated Ringer's)", "Ampicillin or Cefazolin", "Anti-nausea medication"],
        "follow_up": "Monitor electrolytes and glucose. Force feeding if anorexic.",
        "prognosis": "Guarded to Poor depending on severity."
    },
    "Rabies": {
        "treatment_plan": "No cure. Euthanasia is recommended for confirmed cases due to zoonotic risk.",
        "medications": ["None"],
        "follow_up": "Report to local health authorities immediately.",
        "prognosis": "Fatal."
    },
    
    # Bacterial
    "Leptospirosis": {
        "treatment_plan": "Antibiotic therapy and supportive care for kidney/liver function.",
        "medications": ["Doxycycline (drug of choice)", "Penicillin G (for severe cases)"],
        "follow_up": "Monitor renal values (BUN/Creatinine) weekly.",
        "prognosis": "Good if treated early; can lead to chronic kidney failure."
    },
    "Salmonellosis": {
        "treatment_plan": "Fluid therapy and antimicrobials if systemic.",
        "medications": ["Enrofloxacin", "Amoxicillin-clavulanate"],
        "follow_up": "Recheck fecal culture after treatment.",
        "prognosis": "Variable."
    },
    
    # Parasitic
    "Heartworm": {
        "treatment_plan": "Multi-stage protocol (Immiticide). Strict exercise restriction.",
        "medications": ["Melarsomine", "Doxycycline", "Prednisone", "Macrocyclic lactone preventive"],
        "follow_up": "Antigen test 6 months post-treatment.",
        "prognosis": "Good for Class 1-2; Guarded for Class 3-4."
    },
    "Giardia": {
        "treatment_plan": "Antiparasitic medication and environmental decontamination.",
        "medications": ["Fenbendazole", "Metronidazole"],
        "follow_up": "Retest fecal sample in 2-4 weeks.",
        "prognosis": "Excellent."
    },
    
    # Metabolic
    "Diabetes Mellitus": {
        "treatment_plan": "Insulin therapy and dietary management.",
        "medications": ["Insulin (NPH or Glargine)", "High-fiber diet (dogs)", "Low-carb diet (cats)"],
        "follow_up": "Blood glucose curve every 1-2 weeks initially.",
        "prognosis": "Good with consistent management."
    },
    "Milk Fever": {
        "treatment_plan": "Immediate calcium supplementation.",
        "medications": ["Calcium gluconate (IV slow)", "Oral calcium gel"],
        "follow_up": "Monitor for relapse within 24 hours.",
        "prognosis": "Excellent if treated immediately."
    },
    
    # Musculoskeletal
    "Hip Dysplasia": {
        "treatment_plan": "Weight management, physical therapy, and pain control.",
        "medications": ["NSAIDs (Carprofen/Meloxicam)", "Glucosamine/Chondroitin", "Gabapentin"],
        "follow_up": "Radiographs annually to monitor arthritis.",
        "prognosis": "Managed chronically."
    },
    "Laminitis": {
        "treatment_plan": "Emergency. Cryotherapy (ice boots), stall rest, foot support.",
        "medications": ["Phenylbutazone (Bute)", "Acepromazine (vasodilator)"],
        "follow_up": "Radiographs to check for coffin bone rotation.",
        "prognosis": "Guarded."
    },

    # Respiratory
    "Pneumonia": {
        "treatment_plan": "Oxygen therapy, nebulization, and antibiotics.",
        "medications": ["Doxycycline", "Azithromycin", "Bronchodilators"],
        "follow_up": "Chest X-rays every 2 weeks.",
        "prognosis": "Fair to Good."
    },
    
    # Gastrointestinal
    "Colic": {
        "treatment_plan": "Pain management, hydration, walking. Surgery for displacement/torsion.",
        "medications": ["Flunixin meglumine (Banamine)", "Xylazine", "Mineral oil (via nasogastric tube)"],
        "follow_up": "Monitor manure production.",
        "prognosis": "Variable depending on cause."
    }
}

def get_treatment(disease_name, category="General"):
    """
    Retrieve treatment information for a disease with category-based fallback.
    """
    # 1. Check for specific disease match
    if disease_name in TREATMENT_DB:
        return TREATMENT_DB[disease_name]
    
    # 2. Category-based generic professional advice
    fallbacks = {
        "Viral": {
            "treatment_plan": f"Supportive care is priority for {disease_name}. Viral conditions require hydration and monitoring.",
            "medications": ["IV Fluids", "Anti-inflammatories", "Immune support"],
            "prognosis": "Variable - requires clinical observation."
        },
        "Bacterial": {
            "treatment_plan": f"Empirical antibiotic therapy initiated for {disease_name}. Culture and sensitivity recommended.",
            "medications": ["Broad-spectrum antibiotics", "NSAIDs"],
            "prognosis": "Fair to Good with proper antibiotics."
        },
        "Parasitic": {
            "treatment_plan": f"Antiparasitic protocol for {disease_name}. Environmental control is essential.",
            "medications": ["Specific anthelmintics", "External parasite control"],
            "prognosis": "Excellent with completion of treatment."
        },
        "Metabolic": {
            "treatment_plan": f"Dietary management and hormonal stabilization for {disease_name}.",
            "medications": ["Hormonal supplements", "Specialized prescription diet"],
            "prognosis": "Manageable with long-term care."
        },
        "Respiratory": {
            "treatment_plan": f"Oxygen support and airway management for {disease_name}.",
            "medications": ["Bronchodilators", "Nebulization"],
            "prognosis": "Guarded during acute phase."
        },
        "Gastrointestinal": {
            "treatment_plan": f"Bland diet and gastrointestinal protectants for {disease_name}.",
            "medications": ["Anti-emetics", "Probiotics", "Hydration therapy"],
            "prognosis": "Good with 48-hour stabilization."
        },
        "Musculoskeletal": {
            "treatment_plan": f"Rest and anti-inflammatory support for {disease_name}.",
            "medications": ["NSAIDs", "Glucosamine supplements", "Pain management"],
            "prognosis": "Manageable with restricted activity."
        },
        "Cardiovascular": {
            "treatment_plan": f"Cardiac stabilization and monitoring for {disease_name}. Avoid stress.",
            "medications": ["ACE inhibitors", "Diuretics if needed", "Beta-blockers"],
            "prognosis": "Requires lifelong management and frequent checkups."
        }
    }
    
    return fallbacks.get(category, {
        "treatment_plan": "Consult veterinarian for specific treatment protocols.",
        "medications": ["Symptomatic care"],
        "follow_up": "Monitor condition closely.",
        "prognosis": "Unknown"
    })

def save_treatment_db():
    os.makedirs('data', exist_ok=True)
    with open('data/treatment_database.json', 'w') as f:
        json.dump(TREATMENT_DB, f, indent=4)
    print("✅ Treatment database saved.")

if __name__ == "__main__":
    save_treatment_db()
