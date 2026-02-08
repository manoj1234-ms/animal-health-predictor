"""
Enhanced Data Generation Script
Focus: Category-Specific Blood Value Ranges & Symptom Correlation
"""
import pandas as pd
import numpy as np
import os

# Set random seed for reproducibility
np.random.seed(42)

# Full 20 Species
ANIMALS = ['Dog', 'Cat', 'Cattle', 'Pig', 'Sheep', 'Horse', 'Goat', 'Chicken',
           'Rabbit', 'GuineaPig', 'Ferret', 'Parrot', 'Turkey', 'Duck',
           'Lizard', 'Snake', 'Turtle', 'Llama', 'Alpaca', 'Fish']

# Categories & Diseases (Comprehensive List)
CATEGORIES = {
    'Viral': {
        'Dog': ['Canine Distemper', 'Canine Parvovirus', 'Rabies', 'Canine Influenza', 'Kennel Cough'],
        'Cat': ['Feline Panleukopenia', 'Feline Leukemia Virus', 'Feline Herpesvirus', 'Rabies', 'Calicivirus'],
        'Cattle': ['Bovine Viral Diarrhea', 'Foot-and-Mouth Disease', 'Bluetongue', 'Rabies', 'Bovine Herpesvirus'],
        'Pig': ['African Swine Fever', 'Classical Swine Fever', 'Porcine Epidemic Diarrhea', 'PRRS', 'Pseudorabies'],
        'Sheep': ['Bluetongue', 'Rift Valley Fever', 'Contagious Ecthyma', 'Sheep Pox', 'Scrapie'],
        'Horse': ['Equine Influenza', 'Equine Herpesvirus', 'West Nile Virus', 'Rabies', 'Equine Arteritis'],
        'Goat': ['Caprine Arthritis Encephalitis', 'Peste des Petits Ruminants', 'Bluetongue', 'Contagious Ecthyma', 'Rabies'],
        'Chicken': ['Newcastle Disease', 'Avian Influenza', 'Infectious Bronchitis', 'Marek Disease', 'Fowl Pox'],
        'Rabbit': ['Myxomatosis', 'Rabbit Hemorrhagic Disease', 'Rabies', 'Papillomavirus', 'Rotavirus'],
        'GuineaPig': ['Cavian Leukemia', 'Cytomegalovirus', 'Adenovirus', 'Sendai Virus', 'Lymphocytic Choriomeningitis'],
        'Ferret': ['Canine Distemper', 'Influenza', 'Rabies', 'Aleutian Disease', 'Rotavirus'],
        'Parrot': ['Polyomavirus', 'Psittacine Beak Feather Disease', 'Pacheco Disease', 'Proventricular Dilatation', 'Pox Virus'],
        'Turkey': ['Newcastle Disease', 'Avian Influenza', 'Hemorrhagic Enteritis', 'Fowl Pox', 'Turkey Rhinotracheitis'],
        'Duck': ['Duck Virus Hepatitis', 'Duck Plague', 'Avian Influenza', 'Parvovirus', 'Reovirus'],
        'Lizard': ['Adenovirus', 'Herpesvirus', 'Paramyxovirus', 'Iridovirus', 'Ranavirus'],
        'Snake': ['Inclusion Body Disease', 'Paramyxovirus', 'Reovirus', 'Adenovirus', 'Herpesvirus'],
        'Turtle': ['Herpesvirus', 'Ranavirus', 'Iridovirus', 'Picornavirus', 'Adenovirus'],
        'Llama': ['Bluetongue', 'Bovine Viral Diarrhea', 'West Nile Virus', 'Rabies', 'Influenza A'],
        'Alpaca': ['Bluetongue', 'Bovine Viral Diarrhea', 'West Nile Virus', 'Rabies', 'Equine Herpesvirus'],
        'Fish': ['Viral Hemorrhagic Septicemia', 'Infectious Hematopoietic Necrosis', 'Spring Viremia Carp', 'Koi Herpesvirus', 'White Spot Syndrome']
    },
    'Bacterial': {
        'Dog': ['Leptospirosis', 'Bordetella', 'Salmonellosis', 'E.coli Infection', 'Brucellosis'],
        'Cat': ['Salmonellosis', 'E.coli Infection', 'Mycoplasma', 'Campylobacter', 'Chlamydia'],
        'Cattle': ['Brucellosis', 'Tuberculosis', 'Anthrax', 'Leptospirosis', 'Mastitis'],
        'Pig': ['Swine Erysipelas', 'Salmonellosis', 'E.coli Infection', 'Mycoplasma Pneumonia', 'Anthrax'],
        'Sheep': ['Anthrax', 'Tetanus', 'Enterotoxemia', 'Footrot', 'Campylobacteriosis'],
        'Horse': ['Strangles', 'Tetanus', 'Anthrax', 'Salmonellosis', 'Leptospirosis'],
        'Goat': ['Caseous Lymphadenitis', 'Enterotoxemia', 'Tetanus', 'Anthrax', 'Salmonellosis'],
        'Chicken': ['Salmonellosis', 'Fowl Cholera', 'Mycoplasma', 'E.coli Infection', 'Botulism'],
        'Rabbit': ['Pasteurellosis', 'Salmonellosis', 'E.coli Infection', 'Tyzzer Disease', 'Pseudotuberculosis'],
        'GuineaPig': ['Streptococcus Pneumonia', 'Bordetella Bronchiseptica', 'Salmonellosis', 'E.coli', 'Yersiniosis'],
        'Ferret': ['Mycobacterium', 'Salmonellosis', 'Campylobacter', 'Helicobacter', 'E.coli'],
        'Parrot': ['Psittacosis', 'Mycobacteriosis', 'Salmonellosis', 'E.coli', 'Clostridium'],
        'Turkey': ['Fowl Cholera', 'Fowl Typhoid', 'Salmonellosis', 'Mycoplasma', 'E.coli'],
        'Duck': ['Riemerella Anatipestifer', 'Avian Cholera', 'Salmonellosis', 'E.coli', 'Pasteurellosis'],
        'Lizard': ['Salmonellosis', 'Mycobacteriosis', 'Aeromonas', 'Pseudomonas', 'Chlamydia'],
        'Snake': ['Salmonellosis', 'Mycobacteriosis', 'Aeromonas', 'Pseudomonas', 'Septicemia'],
        'Turtle': ['Salmonellosis', 'Mycobacteriosis', 'Aeromonas', 'Shell Rot Bacteria', 'Pseudomonas'],
        'Llama': ['Clostridium Perfringens', 'Tuberculosis', 'Johne Disease', 'Anthrax', 'Brucellosis'],
        'Alpaca': ['Clostridium Perfringens', 'Tuberculosis', 'Johne Disease', 'Anthrax', 'Brucellosis'],
        'Fish': ['Aeromonas Infection', 'Edwardsiella', 'Vibriosis', 'Mycobacteriosis', 'Columnaris']
    },
    'Parasitic': {
        'Dog': ['Roundworm', 'Hookworm', 'Tapeworm', 'Giardia', 'Heartworm'],
        'Cat': ['Roundworm', 'Hookworm', 'Tapeworm', 'Giardia', 'Toxoplasmosis'],
        'Cattle': ['Liver Fluke', 'Lungworm', 'Roundworm', 'Coccidiosis', 'Theileriosis'],
        'Pig': ['Ascariasis', 'Trichinosis', 'Coccidiosis', 'Sarcoptic Mange', 'Toxoplasmosis'],
        'Sheep': ['Liver Fluke', 'Lungworm', 'Coccidiosis', 'Haemonchus', 'Tapeworm'],
        'Horse': ['Strongyles', 'Ascarids', 'Tapeworm', 'Threadworm', 'Stomach Bots'],
        'Goat': ['Haemonchus', 'Liver Fluke', 'Coccidiosis', 'Lungworm', 'Tapeworm'],
        'Chicken': ['Coccidiosis', 'Roundworm', 'Tapeworm', 'Capillaria', 'Gapeworm'],
        'Rabbit': ['Coccidia', 'Pinworms', 'Ear Mites', 'Fur Mites', 'Encephalitozoon Cuniculi'],
        'GuineaPig': ['Coccidia', 'Cryptosporidium', 'Giardia', 'Trixacarus Mites', 'Lice'],
        'Ferret': ['Heartworm', 'Giardia', 'Coccidia', 'Ear Mites', 'Fleas'],
        'Parrot': ['Giardia', 'Coccidia', 'Air Sac Mites', 'Feather Mites', 'Scaly Face Mites'],
        'Turkey': ['Histomoniasis', 'Coccidiosis', 'Roundworm', 'Capillaria', 'Tapeworm'],
        'Duck': ['Renal Coccidiosis', 'Gapeworm', 'Roundworm', 'Tapeworm', 'External Parasites'],
        'Lizard': ['Coccidia', 'Cryptosporidium', 'Mites', 'Ticks', 'Internal Worms'],
        'Snake': ['Mites', 'Ticks', 'Cryptosporidium', 'Coccidia', 'Internal Worms'],
        'Turtle': ['Flagellates', 'Coccidia', 'Roundworms', 'Leeches', 'Mites'],
        'Llama': ['Coccidia', 'Internal Worms', 'Liver Fluke', 'Lice', 'Mites'],
        'Alpaca': ['Coccidia', 'Internal Worms', 'Liver Fluke', 'Lice', 'Meningeal Worm'],
        'Fish': ['Ichthyophthirius', 'Gyrodactylus', 'Dactylogyrus', 'Anchor Worm', 'Fish Lice']
    },
    'Metabolic': {
        'Dog': ['Diabetes Mellitus', 'Kidney Disease', 'Liver Disease', 'Hypothyroidism', 'Cushings Disease'],
        'Cat': ['Diabetes Mellitus', 'Chronic Kidney Disease', 'Hyperthyroidism', 'Liver Disease', 'Fatty Liver'],
        'Cattle': ['Milk Fever', 'Ketosis', 'Hypomagnesemia', 'Bloat', 'Acetonemia'],
        'Pig': ['Gastric Ulcers', 'Edema Disease', 'Hepatosis Dietetica', 'Mulberry Heart', 'Hypoglycemia'],
        'Sheep': ['Pregnancy Toxemia', 'Hypocalcemia', 'White Muscle Disease', 'Urolithiasis', 'Acidosis'],
        'Horse': ['Laminitis', 'Equine Metabolic Syndrome', 'Colic', 'Gastric Ulcers', 'Liver Disease'],
        'Goat': ['Pregnancy Toxemia', 'Hypocalcemia', 'Ketosis', 'Urolithiasis', 'Copper Deficiency'],
        'Chicken': ['Fatty Liver Syndrome', 'Gout', 'Rickets', 'Cage Layer Fatigue', 'Ascites'],
        'Rabbit': ['Obesity', 'Fatty Liver', 'Ketosis', 'Hypocalcemia', 'Urolithiasis'],
        'GuineaPig': ['Scurvy', 'Pregnancy Toxemia', 'Ketosis', 'Urinary Calculi', 'Hypocalcemia'],
        'Ferret': ['Insulinoma', 'Adrenal Disease', 'Hypoglycemia', 'Liver Disease', 'Kidney Disease'],
        'Parrot': ['Hypocalcemia', 'Hypovitaminosis A', 'Gout', 'Fatty Liver', 'Obesity'],
        'Turkey': ['Ascites Syndrome', 'Perosis', 'Fatty Liver', 'Gout', 'Rickets'],
        'Duck': ['Angel Wing', 'Fatty Liver', 'Gout', 'Rickets', 'Nutritional Myopathy'],
        'Lizard': ['Metabolic Bone Disease', 'Hypocalcemia', 'Gout', 'Kidney Disease', 'Hypovitaminosis A'],
        'Snake': ['Hypocalcemia', 'Gout', 'Kidney Disease', 'Fatty Liver', 'Nutritional Deficiencies'],
        'Turtle': ['Metabolic Bone Disease', 'Hypocalcemia', 'Hypovitaminosis A', 'Gout', 'Kidney Disease'],
        'Llama': ['Hepatic Lipidosis', 'Hypocalcemia', 'Ketosis', 'Copper Deficiency', 'Selenium Deficiency'],
        'Alpaca': ['Hepatic Lipidosis', 'Hypocalcemia', 'Ketosis', 'Copper Deficiency', 'Rickets'],
        'Fish': ['Fatty Liver', 'Swim Bladder Disorder', 'Dropsy', 'Malnutrition', 'Vitamin Deficiency']
    },
    'Respiratory': {
        'Dog': ['Pneumonia', 'Bronchitis', 'Tracheal Collapse', 'Laryngeal Paralysis', 'Pulmonary Edema'],
        'Cat': ['Feline Asthma', 'Pneumonia', 'Pleural Effusion', 'Bronchitis', 'URI Complex'],
        'Cattle': ['Bovine Pneumonia', 'Shipping Fever', 'Calf Pneumonia', 'Bronchitis', 'Pulmonary Emphysema'],
        'Pig': ['Enzootic Pneumonia', 'Pleuropneumonia', 'Atrophic Rhinitis', 'Pneumonia', 'Bronchitis'],
        'Sheep': ['Pneumonia', 'Pasteurellosis', 'Lungworm Disease', 'Chronic Bronchitis', 'Adenomatosis'],
        'Horse': ['Equine Asthma', 'Pneumonia', 'COPD', 'Bronchitis', 'Pleuropneumonia'],
        'Goat': ['Pneumonia', 'Bronchitis', 'Pasteurellosis', 'Lungworm Disease', 'Pleuropneumonia'],
        'Chicken': ['Infectious Bronchitis', 'Chronic Respiratory Disease', 'Airsacculitis', 'Pneumonia', 'Aspergillosis'],
        'Rabbit': ['Pasteurellosis', 'Pneumonia', 'Snuffles', 'Bronchitis', 'Aspergillosis'],
        'GuineaPig': ['Pneumonia', 'URI Complex', 'Bronchitis', 'Bordetella Infection', 'Streptococcus Lung Infection'],
        'Ferret': ['Influenza', 'Pneumonia', 'Aspergillosis', 'Bronchitis', 'Pleural Effusion'],
        'Parrot': ['Aspergillosis', 'Airsacculitis', 'Pneumonia', 'Sinusitis', 'Bronchitis'],
        'Turkey': ['Airsacculitis', 'Mycoplasmosis', 'Pneumonia', 'Turkey Rhinotracheitis', 'Aspergillosis'],
        'Duck': ['Aspergillosis', 'Airsacculitis', 'Pneumonia', 'Sinusitis', 'Bronchitis'],
        'Lizard': ['Pneumonia', 'Respiratory Infection', 'Mouth Rot Secondary', 'Aspergillosis', 'Bacterial URI'],
        'Snake': ['Pneumonia', 'Respiratory Infection', 'Inclusion Body Disease Respiratory', 'Aspergillosis', 'Bacterial URI'],
        'Turtle': ['Pneumonia', 'Respiratory Infection', 'URI Complex', 'Aspergillosis', 'Bacterial Infection'],
        'Llama': ['Pneumonia', 'Bronchitis', 'Influenza', 'Aspergillosis', 'Pleuropneumonia'],
        'Alpaca': ['Pneumonia', 'Bronchitis', 'Influenza', 'Aspergillosis', 'Pleuropneumonia'],
        'Fish': ['Gill Disease', 'Bacterial Gill Disease', 'Fungal Gill Infection', 'Branchiomycosis', 'Gill Hyperplasia']
    },
    'Cardiovascular': {
        'Dog': ['Dilated Cardiomyopathy', 'Mitral Valve Disease', 'Congestive Heart Failure', 'Arrhythmia', 'Pericardial Effusion'],
        'Cat': ['Hypertrophic Cardiomyopathy', 'Congestive Heart Failure', 'Thromboembolism', 'Arrhythmia', 'Myocarditis'],
        'Cattle': ['Pericarditis', 'Endocarditis', 'Myocarditis', 'Valvular Disease', 'Arrhythmia'],
        'Pig': ['Mulberry Heart Disease', 'Pericarditis', 'Endocarditis', 'Arrhythmia', 'Myocarditis'],
        'Sheep': ['Endocarditis', 'Pericarditis', 'Myocarditis', 'Valvular Disease', 'Arrhythmia'],
        'Horse': ['Atrial Fibrillation', 'Valvular Disease', 'Myocarditis', 'Pericarditis', 'Arrhythmia'],
        'Goat': ['Endocarditis', 'Pericarditis', 'Myocarditis', 'Valvular Disease', 'Arrhythmia'],
        'Chicken': ['Ascites Syndrome', 'Round Heart Disease', 'Endocarditis', 'Myocarditis', 'Pericarditis'],
        'Rabbit': ['Cardiomyopathy', 'Arrhythmia', 'Endocarditis', 'Heart Failure', 'Myocarditis'],
        'GuineaPig': ['Cardiomyopathy', 'Endocarditis', 'Heart Failure', 'Arrhythmia', 'Pericarditis'],
        'Ferret': ['Dilated Cardiomyopathy', 'Heart Failure', 'Valvular Disease', 'Arrhythmia', 'Heartworm Disease'],
        'Parrot': ['Atherosclerosis', 'Cardiomyopathy', 'Endocarditis', 'Heart Failure', 'Arrhythmia'],
        'Turkey': ['Aortic Rupture', 'Cardiomyopathy', 'Pericarditis', 'Endocarditis', 'Dissecting Aneurysm'],
        'Duck': ['Cardiomyopathy', 'Pericarditis', 'Endocarditis', 'Arrhythmia', 'Heart Failure'],
        'Lizard': ['Cardiomyopathy', 'Myocarditis', 'Endocarditis', 'Heart Failure', 'Arrhythmia'],
        'Snake': ['Cardiomyopathy', 'Myocarditis', 'Endocarditis', 'Septicemia Heart', 'Arrhythmia'],
        'Turtle': ['Cardiomyopathy', 'Myocarditis', 'Endocarditis', 'Heart Failure', 'Septic Carditis'],
        'Llama': ['Endocarditis', 'Pericarditis', 'Myocarditis', 'Valvular Disease', 'Arrhythmia'],
        'Alpaca': ['Endocarditis', 'Pericarditis', 'Myocarditis', 'Valvular Disease', 'Arrhythmia'],
        'Fish': ['Cardiomyopathy', 'Pericarditis', 'Myocarditis', 'Heart Parasites', 'Septic Carditis']
    },
    'Musculoskeletal': {
        'Dog': ['Hip Dysplasia', 'Arthritis', 'Cruciate Ligament Rupture', 'Patellar Luxation', 'Osteochondrosis'],
        'Cat': ['Arthritis', 'Hip Dysplasia', 'Osteochondrodysplasia', 'Fractures', 'Muscular Dystrophy'],
        'Cattle': ['Lameness', 'Laminitis', 'Footrot', 'Arthritis', 'White Muscle Disease'],
        'Pig': ['Arthritis', 'Lameness', 'Osteochondrosis', 'Leg Weakness', 'Fractures'],
        'Sheep': ['Footrot', 'Foot Abscess', 'Laminitis', 'Arthritis', 'White Muscle Disease'],
        'Horse': ['Navicular Disease', 'Laminitis', 'Arthritis', 'Tendon Injuries', 'Fractures'],
        'Goat': ['Arthritis', 'Footrot', 'Laminitis', 'Fractures', 'White Muscle Disease'],
        'Chicken': ['Leg Weakness', 'Rickets', 'Arthritis', 'Perosis', 'Tendon Rupture'],
        'Rabbit': ['Pododermatitis', 'Arthritis', 'Spondylosis', 'Fractures', 'Muscular Dystrophy'],
        'GuineaPig': ['Pododermatitis', 'Arthritis', 'Fractures', 'Muscular Dystrophy', 'Scurvy Joints'],
        'Ferret': ['Osteochondrosis', 'Arthritis', 'Fractures', 'Spinal Disease', 'Muscular Dystrophy'],
        'Parrot': ['Fractures', 'Arthritis', 'Gout Joints', 'Bumblefoot', 'Perosis'],
        'Turkey': ['Arthritis', 'Osteoarthritis', 'Septic Arthritis', 'Leg Weakness', 'Perosis'],
        'Duck': ['Bumblefoot', 'Arthritis', 'Leg Weakness', 'Fractures', 'Lameness'],
        'Lizard': ['Metabolic Bone Disease', 'Fractures', 'Gout', 'Arthritis', 'Spinal Deformity'],
        'Snake': ['Inclusion Body Disease', 'Spinal Arthritis', 'Fractures', 'Kinking', 'Muscular Atrophy'],
        'Turtle': ['Shell Pyramiding', 'Metabolic Bone Disease', 'Fractures', 'Arthritis', 'Soft Shell'],
        'Llama': ['Arthritis', 'Foot Rot', 'Laminitis', 'Fractures', 'White Muscle Disease'],
        'Alpaca': ['Arthritis', 'Foot Rot', 'Laminitis', 'Fractures', 'White Muscle Disease'],
        'Fish': ['Spinal Deformity', 'Fractures', 'Swim Bladder Issues', 'Fin Rot', 'Skeletal Anomalies']
    },
    'Gastrointestinal': {
        'Dog': ['Gastroenteritis', 'Pancreatitis', 'IBD', 'Colitis', 'Gastric Dilation'],
        'Cat': ['Inflammatory Bowel Disease', 'Pancreatitis', 'Megacolon', 'Gastritis', 'Enterocolitis'],
        'Cattle': ['Bloat', 'Displaced Abomasum', 'Rumen Acidosis', 'Hardware Disease', 'Johne Disease'],
        'Pig': ['Transmissible Gastroenteritis', 'Swine Dysentery', 'Proliferative Enteropathy', 'Colitis', 'Gastric Ulcers'],
        'Sheep': ['Enterotoxemia', 'Acidosis', 'Bloat', 'Abomasal Impaction', 'Johne Disease'],
        'Horse': ['Colic', 'Gastric Ulcers', 'Enterocolitis', 'Diarrhea', 'Impaction'],
        'Goat': ['Enterotoxemia', 'Acidosis', 'Bloat', 'Abomasal Impaction', 'Diarrhea'],
        'Chicken': ['Necrotic Enteritis', 'Coccidiosis GI', 'Impacted Crop', 'Sour Crop', 'Pendulous Crop'],
        'Rabbit': ['GI Stasis', 'Enterotoxemia', 'Hairballs', 'Bloat', 'Enterocolitis'],
        'GuineaPig': ['GI Stasis', 'Enterotoxemia', 'Bloat', 'Diarrhea', 'Salmonella Enteritis'],
        'Ferret': ['Proliferative Colitis', 'ECE', 'Gastric Ulcers', 'Helicobacter', 'Intestinal Blockage'],
        'Parrot': ['Proventricular Dilatation', 'Enteritis', 'Candidiasis GI', 'Impacted Crop', 'Giardiasis'],
        'Turkey': ['Enteritis', 'Blue Comb', 'Coccidiosis GI', 'Hemorrhagic Enteritis', 'Ulcerative Enteritis'],
        'Duck': ['Enteritis', 'Botulism', 'Impacted Crop', 'Sour Crop', 'Coccidiosis GI'],
        'Lizard': ['Dysbiosis', 'Parasitic Enteritis', 'Cryptosporidiosis', 'Impaction', 'Anorexia'],
        'Snake': ['Inclusion Body Disease GI', 'Cryptosporidiosis', 'Regurgitation', 'Impaction', 'Parasitic Enteritis'],
        'Turtle': ['Anorexia', 'Enteritis', 'Coccidiosis GI', 'Impaction', 'Dysbiosis'],
        'Llama': ['Gastric Ulcers', 'Enterotoxemia', 'Acidosis', 'Diarrhea', 'Johne Disease'],
        'Alpaca': ['Gastric Ulcers', 'Enterotoxemia', 'Acidosis', 'Diarrhea', 'Johne Disease'],
        'Fish': ['Dropsy', 'Enteritis', 'Bloat', 'Constipation', 'Intestinal Blockage']
    }
}

def generate_blood_values(category, disease=""):
    # Base Values
    wbc = np.random.uniform(6, 17)
    rbc = np.random.uniform(5.5, 8.5)
    hb = np.random.uniform(12, 18)
    plt = np.random.uniform(200, 500)
    glucose = np.random.uniform(80, 110)
    alt = np.random.uniform(10, 55)
    ast = np.random.uniform(10, 55)
    urea = np.random.uniform(7, 27)
    creat = np.random.uniform(0.5, 1.4)
    
    # Category-specific rules
    if category == 'Viral':
        wbc = np.random.uniform(15, 25)
    elif category == 'Bacterial':
        wbc = np.random.uniform(20, 30)
        alt = np.random.uniform(60, 150)
        ast = np.random.uniform(60, 150)
    elif category == 'Parasitic':
        rbc = np.random.uniform(3, 5)
        hb = np.random.uniform(7, 11)
    elif category == 'Metabolic':
        if "Diabetes" in disease:
            glucose = np.random.uniform(200, 500)
        elif "Kidney" in disease or "Renal" in disease:
            urea = np.random.uniform(50, 120)
            creat = np.random.uniform(2.5, 6.0)
        else:
            alt = np.random.uniform(100, 300)
    elif category == 'Gastrointestinal':
        urea = np.random.uniform(30, 60)
        
    # Disease-specific unique offsets (to make them distinguishable)
    # We use the hash of the disease name to create a stable, unique offset
    disease_hash = hash(disease) % 100 / 100.0
    wbc += (disease_hash * 5) - 2.5
    rbc += (disease_hash * 2) - 1.0
    
    return {
        'WBC': round(max(0.1, wbc + np.random.normal(0, 0.5)), 1),
        'RBC': round(max(0.1, rbc + np.random.normal(0, 0.2)), 1),
        'Hemoglobin': round(max(1.0, hb + np.random.normal(0, 0.5)), 1),
        'Platelets': round(max(10, plt + np.random.normal(0, 20)), 0),
        'Glucose': round(max(10, glucose + np.random.normal(0, 10)), 0),
        'ALT': round(max(1, alt + np.random.normal(0, 5)), 0),
        'AST': round(max(1, ast + np.random.normal(0, 5)), 0),
        'Urea': round(max(1, urea + np.random.normal(0, 3)), 0),
        'Creatinine': round(max(0.1, creat + np.random.normal(0, 0.2)), 1)
    }

def generate_symptoms(category, disease=""):
    symptoms = {f'Symptom_{s}': 0 for s in ['Fever', 'Lethargy', 'Vomiting', 'Diarrhea', 'WeightLoss', 'SkinLesion', 'Coughing', 'Lameness']}
    
    # Base correlations
    if category == 'Viral' or category == 'Bacterial':
        symptoms['Symptom_Fever'] = 1 if np.random.random() < 0.8 else 0
    if category == 'Respiratory' or "Cough" in disease:
        symptoms['Symptom_Coughing'] = 1 if np.random.random() < 0.9 else 0
    if category == 'Gastrointestinal' or "Enteritis" in disease or "Vomiting" in disease:
        symptoms['Symptom_Vomiting'] = 1 if np.random.random() < 0.7 else 0
        symptoms['Symptom_Diarrhea'] = 1 if np.random.random() < 0.7 else 0
    if "Lameness" in disease or category == 'Musculoskeletal':
        symptoms['Symptom_Lameness'] = 1 if np.random.random() < 0.9 else 0
        
    # Disease-specific symptom signature
    # Ensure each disease has at least one highly characteristic symptom if it belongs to a category
    sig_hash = hash(disease) % 8
    sym_list = ['Fever', 'Lethargy', 'Vomiting', 'Diarrhea', 'WeightLoss', 'SkinLesion', 'Coughing', 'Lameness']
    target_sym = f'Symptom_{sym_list[sig_hash]}'
    if np.random.random() < 0.7:
        symptoms[target_sym] = 1
        
    return symptoms

def generate_enhanced_dataset(n_samples=15000):
    print(f"Generating {n_samples} enhanced samples...")
    data = []
    
    for _ in range(n_samples):
        animal = np.random.choice(ANIMALS)
        category = np.random.choice(list(CATEGORIES.keys()))
        disease = np.random.choice(CATEGORIES[category][animal])
        
        record = {
            'Animal': animal,
            'Age': round(np.random.uniform(0.5, 15), 1),
            'Gender': np.random.choice(['Male', 'Female']),
            'Breed': np.random.choice(['Mixed', 'Purebred'])
        }
        
        record.update(generate_blood_values(category, disease))
        record.update(generate_symptoms(category, disease))
        record['Category'] = category
        record['Disease'] = disease
        
        data.append(record)
        
    df = pd.DataFrame(data)
    
    # Feature Engineering (Priority 1.3)
    # WBC/RBC Ratio
    df['WBC_RBC_Ratio'] = df['WBC'] / df['RBC']
    # ALT/AST Ratio
    df['ALT_AST_Ratio'] = df['ALT'] / df['AST']
    # Urea/Creatinine Ratio
    df['Urea_Creat_Ratio'] = df['Urea'] / df['Creatinine']
    
    return df

if __name__ == "__main__":
    df = generate_enhanced_dataset(15000)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/enhanced_training_data.csv', index=False)
    print("✅ Enhanced definition generated: data/enhanced_training_data.csv")
    print(f"Stats:\n{df['Category'].value_counts()}")
