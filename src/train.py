"""
Enhanced Training Data Generator
Creates comprehensive veterinary disease dataset based on real-world data
"""

import pandas as pd
import numpy as np
import os

# Set random seed for reproducibility
np.random.seed(42)

# Enhanced animal types (now 8 species)
ANIMALS = ['Dog', 'Cat', 'Cattle', 'Pig', 'Sheep', 'Horse', 'Goat', 'Chicken']

# Enhanced disease categories (now 8 categories)
CATEGORIES = {
    'Viral': {
        'Dog': ['Canine Distemper', 'Canine Parvovirus', 'Rabies', 'Canine Influenza', 'Kennel Cough'],
        'Cat': ['Feline Panleukopenia', 'Feline Leukemia Virus', 'Feline Herpesvirus', 'Rabies', 'Calicivirus'],
        'Cattle': ['Bovine Viral Diarrhea', 'Foot-and-Mouth Disease', 'Bluetongue', 'Rabies', 'Bovine Herpesvirus'],
        'Pig': ['African Swine Fever', 'Classical Swine Fever', 'Porcine Epidemic Diarrhea', 'PRRS', 'Pseudorabies'],
        'Sheep': ['Bluetongue', 'Rift Valley Fever', 'Contagious Ecthyma', 'Sheep Pox', 'Scrapie'],
        'Horse': ['Equine Influenza', 'Equine Herpesvirus', 'West Nile Virus', 'Rabies', 'Strangles'],
        'Goat': ['Caprine Arthritis', 'Peste des Petits Ruminants', 'Bluetongue', 'Contagious Ecthyma', 'Rabies'],
        'Chicken': ['Newcastle Disease', 'Avian Influenza', 'Infectious Bronchitis', 'Marek Disease', 'Fowl Pox']
    },
    'Bacterial': {
        'Dog': ['Leptospirosis', 'Bordetella', 'Salmonellosis', 'E.coli Infection', 'Brucellosis'],
        'Cat': ['Salmonellosis', 'E.coli Infection', 'Mycoplasma', 'Campylobacter', 'Chlamydia'],
        'Cattle': ['Brucellosis', 'Tuberculosis', 'Anthrax', 'Leptospirosis', 'Mastitis'],
        'Pig': ['Swine Erysipelas', 'Salmonellosis', 'E.coli Infection', 'Mycoplasma Pneumonia', 'Anthrax'],
        'Sheep': ['Anthrax', 'Tetanus', 'Enterotoxemia', 'Footrot', 'Campylobacteriosis'],
        'Horse': ['Strangles', 'Tetanus', 'Anthrax', 'Salmonellosis', 'Leptospirosis'],
        'Goat': ['Caseous Lymphadenitis', 'Enterotoxemia', 'Tetanus', 'Anthrax', 'Salmonellosis'],
        'Chicken': ['Salmonellosis', 'Fowl Cholera', 'Mycoplasma', 'E.coli Infection', 'Botulism']
    },
    'Parasitic': {
        'Dog': ['Roundworm', 'Hookworm', 'Tapeworm', 'Giardia', 'Heartworm'],
        'Cat': ['Roundworm', 'Hookworm', 'Tapeworm', 'Giardia', 'Toxoplasmosis'],
        'Cattle': ['Liver Fluke', 'Lungworm', 'Roundworm', 'Coccidiosis', 'Theileriosis'],
        'Pig': ['Ascariasis', 'Trichinosis', 'Coccidiosis', 'Sarcoptic Mange', 'Toxoplasmosis'],
        'Sheep': ['Liver Fluke', 'Lungworm', 'Coccidiosis', 'Haemonchus', 'Tapeworm'],
        'Horse': ['Strongyles', 'Ascarids', 'Tapeworm', 'Threadworm', 'Stomach Bots'],
        'Goat': ['Haemonchus', 'Liver Fluke', 'Coccidiosis', 'Lungworm', 'Tapeworm'],
        'Chicken': ['Coccidiosis', 'Roundworm', 'Tapeworm', 'Capillaria', 'Gapeworm']
    },
    'Metabolic': {
        'Dog': ['Diabetes Mellitus', 'Kidney Disease', 'Liver Disease', 'Hypothyroidism', 'Cushings Disease'],
        'Cat': ['Diabetes Mellitus', 'Chronic Kidney Disease', 'Hyperthyroidism', 'Liver Disease', 'Fatty Liver'],
        'Cattle': ['Milk Fever', 'Ketosis', 'Hypomagnesemia', 'Bloat', 'Acetonemia'],
        'Pig': ['Gastric Ulcers', 'Edema Disease', 'Hepatosis Dietetica', 'Mulberry Heart', 'Hypoglycemia'],
        'Sheep': ['Pregnancy Toxemia', 'Hypocalcemia', 'White Muscle Disease', 'Enterotoxemia', 'Urolithiasis'],
        'Horse': ['Laminitis', 'Equine Metabolic Syndrome', 'Colic', 'Gastric Ulcers', 'Liver Disease'],
        'Goat': ['Pregnancy Toxemia', 'Hypocalcemia', 'Ketosis', 'Urolithiasis', 'Copper Deficiency'],
        'Chicken': ['Fatty Liver Syndrome', 'Gout', 'Rickets', 'Cage Layer Fatigue', 'Ascites']
    },
    'Respiratory': {
        'Dog': ['Pneumonia', 'Bronchitis', 'Tracheal Collapse', 'Laryngeal Paralysis', 'Pulmonary Edema'],
        'Cat': ['Feline Asthma', 'Pneumonia', 'Pleural Effusion', 'Bronchitis', 'URI Complex'],
        'Cattle': ['Bovine Pneumonia', 'Shipping Fever', 'Calf Pneumonia', 'Bronchitis', 'Pulmonary Emphysema'],
        'Pig': ['Enzootic Pneumonia', 'Pleuropneumonia', 'Atrophic Rhinitis', 'Pneumonia', 'Bronchitis'],
        'Sheep': ['Pneumonia', 'Pasteurellosis', 'Lungworm Disease', 'Chronic Bronchitis', 'Adenomatosis'],
        'Horse': ['Equine Asthma', 'Pneumonia', 'COPD', 'Bronchitis', 'Pleuropneumonia'],
        'Goat': ['Pneumonia', 'Bronchitis', 'Caseous Lymphadenitis', 'Lungworm Disease', 'Pasteurellosis'],
        'Chicken': ['Infectious Bronchitis', 'Chronic Respiratory Disease', 'Airsacculitis', 'Pneumonia', 'Aspergillosis']
    },
    'Cardiovascular': {
        'Dog': ['Dilated Cardiomyopathy', 'Mitral Valve Disease', 'Congestive Heart Failure', 'Arrhythmia', 'Pericardial Effusion'],
        'Cat': ['Hypertrophic Cardiomyopathy', 'Congestive Heart Failure', 'Thromboembolism', 'Arrhythmia', 'Myocarditis'],
        'Cattle': ['Pericarditis', 'Endocarditis', 'Myocarditis', 'Valvular Disease', 'Arrhythmia'],
        'Pig': ['Mulberry Heart Disease', 'Pericarditis', 'Endocarditis', 'Arrhythmia', 'Myocarditis'],
        'Sheep': ['Endocarditis', 'Pericarditis', 'Myocarditis', 'Valvular Disease', 'Arrhythmia'],
        'Horse': ['Atrial Fibrillation', 'Valvular Disease', 'Myocarditis', 'Pericarditis', 'Arrhythmia'],
        'Goat': ['Endocarditis', 'Pericarditis', 'Myocarditis', 'Valvular Disease', 'Arrhythmia'],
        'Chicken': ['Ascites Syndrome', 'Round Heart Disease', 'Endocarditis', 'Myocarditis', 'Pericarditis']
    },
    'Musculoskeletal': {
        'Dog': ['Hip Dysplasia', 'Arthritis', 'Cruciate Ligament Rupture', 'Patellar Luxation', 'Osteochondrosis'],
        'Cat': ['Arthritis', 'Hip Dysplasia', 'Osteochondrodysplasia', 'Fractures', 'Muscular Dystrophy'],
        'Cattle': ['Lameness', 'Laminitis', 'Footrot', 'Arthritis', 'White Muscle Disease'],
        'Pig': ['Arthritis', 'Lameness', 'Osteochondrosis', 'Leg Weakness', 'Fractures'],
        'Sheep': ['Footrot', 'Foot Abscess', 'Laminitis', 'Arthritis', 'White Muscle Disease'],
        'Horse': ['Navicular Disease', 'Laminitis', 'Arthritis', 'Tendon Injuries', 'Fractures'],
        'Goat': ['Arthritis', 'Footrot', 'Laminitis', 'Fractures', 'White Muscle Disease'],
        'Chicken': ['Leg Weakness', 'Rickets', 'Arthritis', 'Perosis', 'Tendon Rupture']
    },
    'Gastrointestinal': {
        'Dog': ['Gastroenteritis', 'Pancreatitis', 'IBD', 'Colitis', 'Gastric Dilation'],
        'Cat': ['Inflammatory Bowel Disease', 'Pancreatitis', 'Megacolon', 'Gastritis', 'Enterocolitis'],
        'Cattle': ['Bloat', 'Displaced Abomasum', 'Rumen Acidosis', 'Hardware Disease', 'Johne Disease'],
        'Pig': ['Transmissible Gastroenteritis', 'Swine Dysentery', 'Proliferative Enteropathy', 'Colitis', 'Gastric Ulcers'],
        'Sheep': ['Enterotoxemia', 'Acidosis', 'Bloat', 'Abomasal Impaction', 'Johne Disease'],
        'Horse': ['Colic', 'Gastric Ulcers', 'Enterocolitis', 'Diarrhea', 'Impaction'],
        'Goat': ['Enterotoxemia', 'Acidosis', 'Bloat', 'Abomasal Impaction', 'Diarrhea'],
        'Chicken': ['Necrotic Enteritis', 'Coccidiosis', 'Impacted Crop', 'Sour Crop', 'Pendulous Crop']
    }
}

def generate_blood_values(animal, category, disease):
    """Generate realistic blood values based on disease category"""
    # Base normal values
    wbc_base = np.random.uniform(6, 10)
    rbc_base = np.random.uniform(5, 7)
    hb_base = np.random.uniform(12, 16)
    plt_base = np.random.uniform(200, 400)
    glucose_base = np.random.uniform(80, 120)
    alt_base = np.random.uniform(20, 60)
    ast_base = np.random.uniform(20, 60)
    urea_base = np.random.uniform(15, 35)
    creat_base = np.random.uniform(0.8, 1.5)
    
    # Adjust based on category
    if category == 'Viral' or category == 'Bacterial':
        wbc_base *= np.random.uniform(1.2, 2.0)  # Elevated WBC
        plt_base *= np.random.uniform(0.7, 1.0)  # May decrease
    elif category == 'Parasitic':
        wbc_base *= np.random.uniform(1.1, 1.5)  # Moderate elevation
        rbc_base *= np.random.uniform(0.7, 0.9)  # Anemia possible
    elif category == 'Metabolic':
        glucose_base *= np.random.uniform(0.8, 1.5)  # Variable
        alt_base *= np.random.uniform(1.2, 2.5)  # Liver enzymes up
        ast_base *= np.random.uniform(1.2, 2.5)
    elif category == 'Respiratory':
        wbc_base *= np.random.uniform(1.2, 1.8)
        hb_base *= np.random.uniform(0.9, 1.0)
    elif category == 'Cardiovascular':
        rbc_base *= np.random.uniform(0.8, 1.0)
        hb_base *= np.random.uniform(0.8, 1.0)
    elif category == 'Musculoskeletal':
        # Generally normal blood values
        pass
    elif category == 'Gastrointestinal':
        wbc_base *= np.random.uniform(1.1, 1.7)
        glucose_base *= np.random.uniform(0.7, 1.0)
    
    # Add some random variation
    return {
        'WBC': round(wbc_base + np.random.normal(0, 1), 1),
        'RBC': round(rbc_base + np.random.normal(0, 0.5), 1),
        'Hemoglobin': round(hb_base + np.random.normal(0, 1), 1),
        'Platelets': round(plt_base + np.random.normal(0, 30), 0),
        'Glucose': round(glucose_base + np.random.normal(0, 10), 0),
        'ALT': round(alt_base + np.random.normal(0, 10), 0),
        'AST': round(ast_base + np.random.normal(0, 10), 0),
        'Urea': round(urea_base + np.random.normal(0, 5), 0),
        'Creatinine': round(creat_base + np.random.normal(0, 0.2), 1)
    }

def generate_symptoms(category):
    """Generate symptoms based on disease category"""
    symptoms = {
        'Symptom_Fever': 0,
        'Symptom_Lethargy': 0,
        'Symptom_Vomiting': 0,
        'Symptom_Diarrhea': 0,
        'Symptom_WeightLoss': 0,
        'Symptom_SkinLesion': 0,
        'Symptom_Coughing': 0,
        'Symptom_Lameness': 0
    }
    
    # Category-specific symptoms
    if category == 'Viral':
        symptoms['Symptom_Fever'] = np.random.choice([0, 1], p=[0.2, 0.8])
        symptoms['Symptom_Lethargy'] = np.random.choice([0, 1], p=[0.3, 0.7])
    elif category == 'Bacterial':
        symptoms['Symptom_Fever'] = np.random.choice([0, 1], p=[0.1, 0.9])
        symptoms['Symptom_Lethargy'] = np.random.choice([0, 1], p=[0.4, 0.6])
    elif category == 'Parasitic':
        symptoms['Symptom_WeightLoss'] = np.random.choice([0, 1], p=[0.3, 0.7])
        symptoms['Symptom_Diarrhea'] = np.random.choice([0, 1], p=[0.4, 0.6])
    elif category == 'Metabolic':
        symptoms['Symptom_WeightLoss'] = np.random.choice([0, 1], p=[0.4, 0.6])
        symptoms['Symptom_Lethargy'] = np.random.choice([0, 1], p=[0.3, 0.7])
    elif category == 'Respiratory':
        symptoms['Symptom_Coughing'] = np.random.choice([0, 1], p=[0.1, 0.9])
        symptoms['Symptom_Fever'] = np.random.choice([0, 1], p=[0.5, 0.5])
    elif category == 'Cardiovascular':
        symptoms['Symptom_Lethargy'] = np.random.choice([0, 1], p=[0.2, 0.8])
    elif category == 'Musculoskeletal':
        symptoms['Symptom_Lameness'] = np.random.choice([0, 1], p=[0.1, 0.9])
    elif category == 'Gastrointestinal':
        symptoms['Symptom_Vomiting'] = np.random.choice([0, 1], p=[0.3, 0.7])
        symptoms['Symptom_Diarrhea'] = np.random.choice([0, 1], p=[0.2, 0.8])
    
    return symptoms

def create_comprehensive_dataset(n_samples=2000):
    """Create comprehensive training dataset"""
    data = []
    
    print(f"Generating {n_samples} samples across {len(ANIMALS)} species and {len(CATEGORIES)} categories...")
    
    for _ in range(n_samples):
        animal = np.random.choice(ANIMALS)
        category = np.random.choice(list(CATEGORIES.keys()))
        disease = np.random.choice(CATEGORIES[category][animal])
        
        # Basic info
        record = {
            'Animal': animal,
            'Age': round(np.random.uniform(0.5, 15), 1),
            'Gender': np.random.choice(['Male', 'Female']),
            'Breed': np.random.choice(['Mixed', 'Purebred', 'Crossbreed'])
        }
        
        # Blood values
        blood_values = generate_blood_values(animal, category, disease)
        record.update(blood_values)
        
        # Symptoms
        symptoms = generate_symptoms(category)
        record.update(symptoms)
        
        # Labels
        record['Category'] = category
        record['Disease'] = disease
        
        data.append(record)
    
    df = pd.DataFrame(data)
    
    # Summary statistics
    print("\n" + "="*70)
    print("DATASET SUMMARY")
    print("="*70)
    print(f"\nTotal Samples: {len(df)}")
    print(f"\nSpecies Distribution:")
    print(df['Animal'].value_counts().to_string())
    print(f"\nCategory Distribution:")
    print(df['Category'].value_counts().to_string())
    print(f"\nDiseases per Category:")
    for cat in CATEGORIES.keys():
        cat_diseases = df[df['Category'] == cat]['Disease'].nunique()
        print(f"  {cat}: {cat_diseases} diseases")
    
    return df

if __name__ == "__main__":
    # Create dataset
    df = create_comprehensive_dataset(n_samples=2000)
    
    # Save to CSV
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/training_data.csv', index=False)
    
    print(f"\n✅ Dataset saved to data/training_data.csv")
    print(f"📊 Shape: {df.shape}")
    print(f"🏥 Ready for training!\n")
