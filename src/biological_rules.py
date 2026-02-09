"""
Biological validation rules and reference ranges for supported animal species.
Includes vital sign ranges (Temperature, Heart Rate, Respiration) and logic for
detecting abnormalities.
"""

# Reference Ranges for Vital Signs
# Source: Veterinary Manuals (Merck, etc.)
# Temp in Celsius, HR in bpm, RR in breaths/min
VITAL_SIGNS_REFERENCE = {
    'Dog': {
        'temp_min': 37.9, 'temp_max': 39.9,
        'hr_min': 60, 'hr_max': 140,
        'rr_min': 10, 'rr_max': 30,
        'notes': 'HR varies significantly by size (Small dogs higher, Large dogs lower)'
    },
    'Cat': {
        'temp_min': 38.1, 'temp_max': 39.2,
        'hr_min': 140, 'hr_max': 220,
        'rr_min': 20, 'rr_max': 30,
        'notes': 'Stress can rapidly increase HR'
    },
    'Cattle': {
        'temp_min': 38.0, 'temp_max': 39.3,
        'hr_min': 40, 'hr_max': 80,
        'rr_min': 10, 'rr_max': 30,
        'notes': 'Rumen contractions 1-2 per minute'
    },
    'Horse': {
        'temp_min': 37.2, 'temp_max': 38.3,
        'hr_min': 28, 'hr_max': 40,
        'rr_min': 8, 'rr_max': 16,
        'notes': 'Resting HR > 60 is a pain indicator (Colic)'
    },
    'Pig': {
        'temp_min': 38.7, 'temp_max': 39.8,
        'hr_min': 60, 'hr_max': 100,
        'rr_min': 8, 'rr_max': 18,
        'notes': 'Susceptible to heat stress'
    },
    'Sheep': {
        'temp_min': 38.3, 'temp_max': 39.9,
        'hr_min': 70, 'hr_max': 90,
        'rr_min': 12, 'rr_max': 25,
        'notes': 'Pant when stressed'
    },
    'Goat': {
        'temp_min': 38.5, 'temp_max': 39.7,
        'hr_min': 70, 'hr_max': 90,
        'rr_min': 15, 'rr_max': 30,
        'notes': 'Similar to sheep but more active'
    },
    'Chicken': {
        'temp_min': 40.6, 'temp_max': 41.7,
        'hr_min': 250, 'hr_max': 300,
        'rr_min': 12, 'rr_max': 36,
        'notes': 'Very high metabolic rate'
    },
    # --- New Zoo & Buffalo Additions ---
    'Buffalo': {
        'temp_min': 37.5, 'temp_max': 39.0,
        'hr_min': 40, 'hr_max': 80,
        'rr_min': 10, 'rr_max': 30,
        'notes': 'Similar to Cattle but more resilient to heat'
    },
    'Lion': {
        'temp_min': 38.0, 'temp_max': 39.5,
        'hr_min': 40, 'hr_max': 50, # Resting
        'rr_min': 10, 'rr_max': 24,
        'notes': 'Carnivore; stress can spike HR rapidly'
    },
    'Tiger': {
        'temp_min': 37.8, 'temp_max': 39.2,
        'hr_min': 45, 'hr_max': 60,
        'rr_min': 12, 'rr_max': 25,
        'notes': 'Solitary predator; high stress sensitivity in captivity'
    },
    'Elephant': {
        'temp_min': 36.0, 'temp_max': 37.0, # Lower body temp
        'hr_min': 25, 'hr_max': 35,      # Very slow heart rate
        'rr_min': 4, 'rr_max': 12,       # Slow respiration
        'notes': 'Largest land mammal; unique physiology'
    },
    'Giraffe': {
        'temp_min': 38.0, 'temp_max': 39.0,
        'hr_min': 40, 'hr_max': 90,      # High blood pressure adaptation
        'rr_min': 8, 'rr_max': 20,
        'notes': 'Unique cardiovascular system for height'
    },
    # Default for unknowns (Generic Mammal)
    'Unknown': {
        'temp_min': 37.0, 'temp_max': 39.5,
        'hr_min': 60, 'hr_max': 100,
        'rr_min': 10, 'rr_max': 30,
        'notes': 'Generic Reference'
    }
}

def analyze_vitals(animal_type, temp=None, hr=None, rr=None):
    """
    Analyze vital signs against species-specific reference ranges.
    Returns a list of alerts (if any).
    """
    alerts = []
    
    # Normalize animal string (e.g. "Cow" -> "Cattle")
    species_map = {
        'Cow': 'Cattle',
        'Puppy': 'Dog',
        'Kitten': 'Cat',
        'Calf': 'Cattle',
        'Foal': 'Horse'
    }
    animal_key = species_map.get(animal_type, animal_type)
    
    # Fallback if species not found
    if animal_key not in VITAL_SIGNS_REFERENCE:
        ref = VITAL_SIGNS_REFERENCE['Unknown']
        alerts.append({
            'severity': 'INFO',
            'message': f"Species '{animal_type}' not found. Using generic mammal ranges.",
            'param': 'Species'
        })
    else:
        ref = VITAL_SIGNS_REFERENCE[animal_key]

    # Check Temperature
    if temp is not None:
        if temp < ref['temp_min']:
            alerts.append({
                'severity': 'CRITICAL',
                'message': f"Hypothermia Risk: {temp}°C is below normal range ({ref['temp_min']}-{ref['temp_max']}) for {animal_type}",
                'param': 'Temperature'
            })
        elif temp > ref['temp_max']:
            severity = 'CRITICAL' if temp > ref['temp_max'] + 1.0 else 'WARNING'
            alerts.append({
                'severity': severity,
                'message': f"Fever Detected: {temp}°C is above normal range ({ref['temp_min']}-{ref['temp_max']}) for {animal_type}",
                'param': 'Temperature'
            })

    # Check Heart Rate
    if hr is not None:
        if hr < ref['hr_min']:
            alerts.append({
                'severity': 'WARNING',
                'message': f"Bradycardia (Low HR): {hr} bpm is below normal ({ref['hr_min']}-{ref['hr_max']})",
                'param': 'Heart Rate'
            })
        elif hr > ref['hr_max']:
            alerts.append({
                'severity': 'WARNING',
                'message': f"Tachycardia (High HR): {hr} bpm is above normal ({ref['hr_min']}-{ref['hr_max']})",
                'param': 'Heart Rate'
            })

    return {
        'species': animal_key,
        'alerts': alerts,
        'reference_used': ref
    }
