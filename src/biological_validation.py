"""
Enhanced Biological Validation Module
Comprehensive disease compatibility matrix for 20 animal species and 8 disease categories
"""

# Comprehensive disease compatibility matrix
ANIMAL_DISEASE_COMPATIBILITY = {
    'Dog': {
        'Viral': ['Canine Distemper', 'Canine Parvovirus', 'Rabies', 'Canine Influenza', 'Kennel Cough'],
        'Bacterial': ['Leptospirosis', 'Bordetella', 'Salmonellosis', 'E.coli Infection', 'Brucellosis'],
        'Parasitic': ['Roundworm', 'Hookworm', 'Tapeworm', 'Giardia', 'Heartworm'],
        'Metabolic': ['Diabetes Mellitus', 'Kidney Disease', 'Liver Disease', 'Hypothyroidism', 'Cushings Disease'],
        'Respiratory': ['Pneumonia', 'Bronchitis', 'Tracheal Collapse', 'Laryngeal Paralysis', 'Pulmonary Edema'],
        'Cardiovascular': ['Dilated Cardiomyopathy', 'Mitral Valve Disease', 'Congestive Heart Failure', 'Arrhythmia', 'Pericardial Effusion'],
        'Musculoskeletal': ['Hip Dysplasia', 'Arthritis', 'Cruciate Ligament Rupture', 'Patellar Luxation', 'Osteochondrosis'],
        'Gastrointestinal': ['Gastroenteritis', 'Pancreatitis', 'IBD', 'Colitis', 'Gastric Dilation']
    },
    'Cat': {
        'Viral': ['Feline Panleukopenia', 'Feline Leukemia Virus', 'Feline Herpesvirus', 'Rabies', 'Calicivirus'],
        'Bacterial': ['Salmonellosis', 'E.coli Infection', 'Mycoplasma', 'Campylobacter', 'Chlamydia'],
        'Parasitic': ['Roundworm', 'Hookworm', 'Tapeworm', 'Giardia', 'Toxoplasmosis'],
        'Metabolic': ['Diabetes Mellitus', 'Chronic Kidney Disease', 'Hyperthyroidism', 'Liver Disease', 'Fatty Liver'],
        'Respiratory': ['Feline Asthma', 'Pneumonia', 'Pleural Effusion', 'Bronchitis', 'URI Complex'],
        'Cardiovascular': ['Hypertrophic Cardiomyopathy', 'Congestive Heart Failure', 'Thromboembolism', 'Arrhythmia', 'Myocarditis'],
        'Musculoskeletal': ['Arthritis', 'Hip Dysplasia', 'Osteochondrodysplasia', 'Fractures', 'Muscular Dystrophy'],
        'Gastrointestinal': ['Inflammatory Bowel Disease', 'Pancreatitis', 'Megacolon', 'Gastritis', 'Enterocolitis']
    },
    'Cattle': {
        'Viral': ['Bovine Viral Diarrhea', 'Foot-and-Mouth Disease', 'Bluetongue', 'Rabies', 'Bovine Herpesvirus'],
        'Bacterial': ['Brucellosis', 'Tuberculosis', 'Anthrax', 'Leptospirosis', 'Mastitis'],
        'Parasitic': ['Liver Fluke', 'Lungworm', 'Roundworm', 'Coccidiosis', 'Theileriosis'],
        'Metabolic': ['Milk Fever', 'Ketosis', 'Hypomagnesemia', 'Bloat', 'Acetonemia'],
        'Respiratory': ['Bovine Pneumonia', 'Shipping Fever', 'Calf Pneumonia', 'Bronchitis', 'Pulmonary Emphysema'],
        'Cardiovascular': ['Pericarditis', 'Endocarditis', 'Myocarditis', 'Valvular Disease', 'Arrhythmia'],
        'Musculoskeletal': ['Lameness', 'Laminitis', 'Footrot', 'Arthritis', 'White Muscle Disease'],
        'Gastrointestinal': ['Bloat', 'Displaced Abomasum', 'Rumen Acidosis', 'Hardware Disease', 'Johne Disease']
    },
    'Pig': {
        'Viral': ['African Swine Fever', 'Classical Swine Fever', 'Porcine Epidemic Diarrhea', 'PRRS', 'Pseudorabies'],
        'Bacterial': ['Swine Erysipelas', 'Salmonellosis', 'E.coli Infection', 'Mycoplasma Pneumonia', 'Anthrax'],
        'Parasitic': ['Ascariasis', 'Trichinosis', 'Coccidiosis', 'Sarcoptic Mange', 'Toxoplasmosis'],
        'Metabolic': ['Gastric Ulcers', 'Edema Disease', 'Hepatosis Dietetica', 'Mulberry Heart', 'Hypoglycemia'],
        'Respiratory': ['Enzootic Pneumonia', 'Pleuropneumonia', 'Atrophic Rhinitis', 'Pneumonia', 'Bronchitis'],
        'Cardiovascular': ['Mulberry Heart Disease', 'Pericarditis', 'Endocarditis', 'Arrhythmia', 'Myocarditis'],
        'Musculoskeletal': ['Arthritis', 'Lameness', 'Osteochondrosis', 'Leg Weakness', 'Fractures'],
        'Gastrointestinal': ['Transmissible Gastroenteritis', 'Swine Dysentery', 'Proliferative Enteropathy', 'Colitis', 'Gastric Ulcers']
    },
    'Sheep': {
        'Viral': ['Bluetongue', 'Rift Valley Fever', 'Contagious Ecthyma', 'Sheep Pox', 'Scrapie'],
        'Bacterial': ['Anthrax', 'Tetanus', 'Enterotoxemia', 'Footrot', 'Campylobacteriosis'],
        'Parasitic': ['Liver Fluke', 'Lungworm', 'Coccidiosis', 'Haemonchus', 'Tapeworm'],
        'Metabolic': ['Pregnancy Toxemia', 'Hypocalcemia', 'White Muscle Disease', 'Enterotoxemia', 'Urolithiasis'],
        'Respiratory': ['Pneumonia', 'Pasteurellosis', 'Lungworm Disease', 'Chronic Bronchitis', 'Adenomatosis'],
        'Cardiovascular': ['Endocarditis', 'Pericarditis', 'Myocarditis', 'Valvular Disease', 'Arrhythmia'],
        'Musculoskeletal': ['Footrot', 'Foot Abscess', 'Laminitis', 'Arthritis', 'White Muscle Disease'],
        'Gastrointestinal': ['Enterotoxemia', 'Acidosis', 'Bloat', 'Abomasal Impaction', 'Johne Disease']
    },
    'Horse': {
        'Viral': ['Equine Influenza', 'Equine Herpesvirus', 'West Nile Virus', 'Rabies', 'Equine Arteritis'],
        'Bacterial': ['Strangles', 'Tetanus', 'Anthrax', 'Salmonellosis', 'Leptospirosis'],
        'Parasitic': ['Strongyles', 'Ascarids', 'Tapeworm', 'Threadworm', 'Stomach Bots'],
        'Metabolic': ['Laminitis', 'Equine Metabolic Syndrome', 'Colic', 'Gastric Ulcers', 'Liver Disease'],
        'Respiratory': ['Equine Asthma', 'Pneumonia', 'COPD', 'Bronchitis', 'Pleuropneumonia'],
        'Cardiovascular': ['Atrial Fibrillation', 'Valvular Disease', 'Myocarditis', 'Pericarditis', 'Arrhythmia'],
        'Musculoskeletal': ['Navicular Disease', 'Laminitis', 'Arthritis', 'Tendon Injuries', 'Fractures'],
        'Gastrointestinal': ['Colic', 'Gastric Ulcers', 'Enterocolitis', 'Diarrhea', 'Impaction']
    },
    'Goat': {
        'Viral': ['Caprine Arthritis Encephalitis', 'Peste des Petits Ruminants', 'Bluetongue', 'Contagious Ecthyma', 'Rabies'],
        'Bacterial': ['Caseous Lymphadenitis', 'Enterotoxemia', 'Tetanus', 'Anthrax', 'Salmonellosis'],
        'Parasitic': ['Haemonchus', 'Liver Fluke', 'Coccidiosis', 'Lungworm', 'Tapeworm'],
        'Metabolic': ['Pregnancy Toxemia', 'Hypocalcemia', 'Ketosis', 'Urolithiasis', 'Copper Deficiency'],
        'Respiratory': ['Pneumonia', 'Bronchitis', 'Caseous Lymphadenitis', 'Lungworm Disease', 'Pasteurellosis'],
        'Cardiovascular': ['Endocarditis', 'Pericarditis', 'Myocarditis', 'Valvular Disease', 'Arrhythmia'],
        'Musculoskeletal': ['Arthritis', 'Footrot', 'Laminitis', 'Fractures', 'White Muscle Disease'],
        'Gastrointestinal': ['Enterotoxemia', 'Acidosis', 'Bloat', 'Abomasal Impaction', 'Diarrhea']
    },
    'Chicken': {
        'Viral': ['Newcastle Disease', 'Avian Influenza', 'Infectious Bronchitis', 'Marek Disease', 'Fowl Pox'],
        'Bacterial': ['Salmonellosis', 'Fowl Cholera', 'Mycoplasma', 'E.coli Infection', 'Botulism'],
        'Parasitic': ['Coccidiosis', 'Roundworm', 'Tapeworm', 'Capillaria', 'Gapeworm'],
        'Metabolic': ['Fatty Liver Syndrome', 'Gout', 'Rickets', 'Cage Layer Fatigue', 'Ascites'],
        'Respiratory': ['Infectious Bronchitis', 'Chronic Respiratory Disease', 'Airsacculitis', 'Pneumonia', 'Aspergillosis'],
        'Cardiovascular': ['Ascites Syndrome', 'Round Heart Disease', 'Endocarditis', 'Myocarditis', 'Pericarditis'],
        'Musculoskeletal': ['Leg Weakness', 'Rickets', 'Arthritis', 'Perosis', 'Tendon Rupture'],
        'Gastrointestinal': ['Necrotic Enteritis', 'Coccidiosis', 'Impacted Crop', 'Sour Crop', 'Pendulous Crop']
    },
    'Rabbit': {
        'Viral': ['Myxomatosis', 'Rabbit Hemorrhagic Disease', 'Rabies', 'Papillomavirus', 'Rotavirus'],
        'Bacterial': ['Pasteurellosis', 'Salmonellosis', 'E.coli Infection', 'Tyzzer Disease', 'Pseudotuberculosis'],
        'Parasitic': ['Coccidia', 'Pinworms', 'Ear Mites', 'Fur Mites', 'Encephalitozoon Cuniculi'],
        'Metabolic': ['Obesity', 'Fatty Liver', 'Ketosis', 'Hypocalcemia', 'Urolithiasis'],
        'Respiratory': ['Pasteurellosis', 'Pneumonia', 'Snuffles', 'Bronchitis', 'Aspergillosis'],
        'Cardiovascular': ['Cardiomyopathy', 'Arrhythmia', 'Endocarditis', 'Heart Failure', 'Myocarditis'],
        'Musculoskeletal': ['Pododermatitis', 'Arthritis', 'Spondylosis', 'Fractures', 'Muscular Dystrophy'],
        'Gastrointestinal': ['GI Stasis', 'Enterotoxemia', 'Hairballs', 'Bloat', 'Enterocolitis']
    },
    'GuineaPig': {
        'Viral': ['Cavian Leukemia', 'Cytomegalovirus', 'Adenovirus', 'Sendai Virus', 'Lymphocytic Choriomeningitis'],
        'Bacterial': ['Streptococcus Pneumonia', 'Bordetella Bronchiseptica', 'Salmonellosis', 'E.coli', 'Yersiniosis'],
        'Parasitic': ['Coccidia', 'Cryptosporidium', 'Giardia', 'Trixacarus Mites', 'Lice'],
        'Metabolic': ['Scurvy', 'Pregnancy Toxemia', 'Ketosis', 'Urinary Calculi', 'Hypocalcemia'],
        'Respiratory': ['Pneumonia', 'URI Complex', 'Bronchitis', 'Bordetella Infection', 'Streptococcus Lung Infection'],
        'Cardiovascular': ['Cardiomyopathy', 'Endocarditis', 'Heart Failure', 'Arrhythmia', 'Pericarditis'],
        'Musculoskeletal': ['Pododermatitis', 'Arthritis', 'Fractures', 'Muscular Dystrophy', 'Scurvy Joints'],
        'Gastrointestinal': ['GI Stasis', 'Enterotoxemia', 'Bloat', 'Diarrhea', 'Salmonella Enteritis']
    },
    'Ferret': {
        'Viral': ['Canine Distemper', 'Influenza', 'Rabies', 'Aleutian Disease', 'Rotavirus'],
        'Bacterial': ['Mycobacterium', 'Salmonellosis', 'Campylobacter', 'Helicobacter', 'E.coli'],
        'Parasitic': ['Heartworm', 'Giardia', 'Coccidia', 'Ear Mites', 'Fleas'],
        'Metabolic': ['Insulinoma', 'Adrenal Disease', 'Hypoglycemia', 'Liver Disease', 'Kidney Disease'],
        'Respiratory': ['Influenza', 'Pneumonia', 'Aspergillosis', 'Bronchitis', 'Pleural Effusion'],
        'Cardiovascular': ['Dilated Cardiomyopathy', 'Heart Failure', 'Valvular Disease', 'Arrhythmia', 'Heartworm Disease'],
        'Musculoskeletal': ['Osteochondrosis', 'Arthritis', 'Fractures', 'Spinal Disease', 'Muscular Dystrophy'],
        'Gastrointestinal': ['Proliferative Colitis', 'ECE', 'Gastric Ulcers', 'Helicobacter', 'Intestinal Blockage']
    },
    'Parrot': {
        'Viral': ['Polyomavirus', 'Psittacine Beak Feather Disease', 'Pacheco Disease', 'Proventricular Dilatation', 'Pox Virus'],
        'Bacterial': ['Psittacosis', 'Mycobacteriosis', 'Salmonellosis', 'E.coli', 'Clostridium'],
        'Parasitic': ['Giardia', 'Coccidia', 'Air Sac Mites', 'Feather Mites', 'Scaly Face Mites'],
        'Metabolic': ['Hypocalcemia', 'Hypovitaminosis A', 'Gout', 'Fatty Liver', 'Obesity'],
        'Respiratory': ['Aspergillosis', 'Airsacculitis', 'Pneumonia', 'Sinusitis', 'Bronchitis'],
        'Cardiovascular': ['Atherosclerosis', 'Cardiomyopathy', 'Endocarditis', 'Heart Failure', 'Arrhythmia'],
        'Musculoskeletal': ['Fractures', 'Arthritis', 'Gout Joints', 'Bumblefoot', 'Perosis'],
        'Gastrointestinal': ['Proventricular Dilatation', 'Enteritis', 'Candidiasis GI', 'Impacted Crop', 'Giardiasis']
    },
    'Turkey': {
        'Viral': ['Newcastle Disease', 'Avian Influenza', 'Hemorrhagic Enteritis', 'Fowl Pox', 'Turkey Rhinotracheitis'],
        'Bacterial': ['Fowl Cholera', 'Fowl Typhoid', 'Salmonellosis', 'Mycoplasma', 'E.coli'],
        'Parasitic': ['Histomoniasis', 'Coccidiosis', 'Roundworm', 'Capillaria', 'Tapeworm'],
        'Metabolic': ['Ascites Syndrome', 'Perosis', 'Fatty Liver', 'Gout', 'Rickets'],
        'Respiratory': ['Airsacculitis', 'Mycoplasmosis', 'Pneumonia', 'Turkey Rhinotracheitis', 'Aspergillosis'],
        'Cardiovascular': ['Aortic Rupture', 'Cardiomyopathy', 'Pericarditis', 'Endocarditis', 'Dissecting Aneurysm'],
        'Musculoskeletal': ['Arthritis', 'Osteoarthritis', 'Septic Arthritis', 'Leg Weakness', 'Perosis'],
        'Gastrointestinal': ['Enteritis', 'Blue Comb', 'Coccidiosis GI', 'Hemorrhagic Enteritis', 'Ulcerative Enteritis']
    },
    'Duck': {
        'Viral': ['Duck Virus Hepatitis', 'Duck Plague', 'Avian Influenza', 'Parvovirus', 'Reovirus'],
        'Bacterial': ['Riemerella Anatipestifer', 'Avian Cholera', 'Salmonellosis', 'E.coli', 'Pasteurellosis'],
        'Parasitic': ['Renal Coccidiosis', 'Gapeworm', 'Roundworm', 'Tapeworm', 'External Parasites'],
        'Metabolic': ['Angel Wing', 'Fatty Liver', 'Gout', 'Rickets', 'Nutritional Myopathy'],
        'Respiratory': ['Aspergillosis', 'Airsacculitis', 'Pneumonia', 'Sinusitis', 'Bronchitis'],
        'Cardiovascular': ['Cardiomyopathy', 'Pericarditis', 'Endocarditis', 'Arrhythmia', 'Heart Failure'],
        'Musculoskeletal': ['Bumblefoot', 'Arthritis', 'Leg Weakness', 'Fractures', 'Lameness'],
        'Gastrointestinal': ['Enteritis', 'Botulism', 'Impacted Crop', 'Sour Crop', 'Coccidiosis GI']
    },
    'Lizard': {
        'Viral': ['Adenovirus', 'Herpesvirus', 'Paramyxovirus', 'Iridovirus', 'Ranavirus'],
        'Bacterial': ['Salmonellosis', 'Mycobacteriosis', 'Aeromonas', 'Pseudomonas', 'Chlamydia'],
        'Parasitic': ['Coccidia', 'Cryptosporidium', 'Mites', 'Ticks', 'Internal Worms'],
        'Metabolic': ['Metabolic Bone Disease', 'Hypocalcemia', 'Gout', 'Kidney Disease', 'Hypovitaminosis A'],
        'Respiratory': ['Pneumonia', 'Respiratory Infection', 'Mouth Rot Secondary', 'Aspergillosis', 'Bacterial URI'],
        'Cardiovascular': ['Cardiomyopathy', 'Myocarditis', 'Endocarditis', 'Heart Failure', 'Arrhythmia'],
        'Musculoskeletal': ['Metabolic Bone Disease', 'Fractures', 'Gout', 'Arthritis', 'Spinal Deformity'],
        'Gastrointestinal': ['Dysbiosis', 'Parasitic Enteritis', 'Cryptosporidiosis', 'Impaction', 'Anorexia']
    },
    'Snake': {
        'Viral': ['Inclusion Body Disease', 'Paramyxovirus', 'Reovirus', 'Adenovirus', 'Herpesvirus'],
        'Bacterial': ['Salmonellosis', 'Mycobacteriosis', 'Aeromonas', 'Pseudomonas', 'Septicemia'],
        'Parasitic': ['Mites', 'Ticks', 'Cryptosporidium', 'Coccidia', 'Internal Worms'],
        'Metabolic': ['Hypocalcemia', 'Gout', 'Kidney Disease', 'Fatty Liver', 'Nutritional Deficiencies'],
        'Respiratory': ['Pneumonia', 'Respiratory Infection', 'Inclusion Body Disease Respiratory', 'Aspergillosis', 'Bacterial URI'],
        'Cardiovascular': ['Cardiomyopathy', 'Myocarditis', 'Endocarditis', 'Septicemia Heart', 'Arrhythmia'],
        'Musculoskeletal': ['Inclusion Body Disease', 'Spinal Arthritis', 'Fractures', 'Kinking', 'Muscular Atrophy'],
        'Gastrointestinal': ['Inclusion Body Disease GI', 'Cryptosporidiosis', 'Regurgitation', 'Impaction', 'Parasitic Enteritis']
    },
    'Turtle': {
        'Viral': ['Herpesvirus', 'Ranavirus', 'Iridovirus', 'Picornavirus', 'Adenovirus'],
        'Bacterial': ['Salmonellosis', 'Mycobacteriosis', 'Aeromonas', 'Shell Rot Bacteria', 'Pseudomonas'],
        'Parasitic': ['Flagellates', 'Coccidia', 'Roundworms', 'Leeches', 'Mites'],
        'Metabolic': ['Metabolic Bone Disease', 'Hypocalcemia', 'Hypovitaminosis A', 'Gout', 'Kidney Disease'],
        'Respiratory': ['Pneumonia', 'Respiratory Infection', 'URI Complex', 'Aspergillosis', 'Bacterial Infection'],
        'Cardiovascular': ['Cardiomyopathy', 'Myocarditis', 'Endocarditis', 'Heart Failure', 'Septic Carditis'],
        'Musculoskeletal': ['Shell Pyramiding', 'Metabolic Bone Disease', 'Fractures', 'Arthritis', 'Soft Shell'],
        'Gastrointestinal': ['Anorexia', 'Enteritis', 'Coccidiosis GI', 'Impaction', 'Dysbiosis']
    },
    'Llama': {
        'Viral': ['Bluetongue', 'Bovine Viral Diarrhea', 'West Nile Virus', 'Rabies', 'Influenza A'],
        'Bacterial': ['Clostridium Perfringens', 'Tuberculosis', 'Johne Disease', 'Anthrax', 'Brucellosis'],
        'Parasitic': ['Coccidia', 'Internal Worms', 'Liver Fluke', 'Lice', 'Mites'],
        'Metabolic': ['Hepatic Lipidosis', 'Hypocalcemia', 'Ketosis', 'Copper Deficiency', 'Selenium Deficiency'],
        'Respiratory': ['Pneumonia', 'Bronchitis', 'Influenza', 'Aspergillosis', 'Pleuropneumonia'],
        'Cardiovascular': ['Endocarditis', 'Pericarditis', 'Myocarditis', 'Valvular Disease', 'Arrhythmia'],
        'Musculoskeletal': ['Arthritis', 'Foot Rot', 'Laminitis', 'Fractures', 'White Muscle Disease'],
        'Gastrointestinal': ['Gastric Ulcers', 'Enterotoxemia', 'Acidosis', 'Diarrhea', 'Johne Disease']
    },
    'Alpaca': {
        'Viral': ['Bluetongue', 'Bovine Viral Diarrhea', 'West Nile Virus', 'Rabies', 'Equine Herpesvirus'],
        'Bacterial': ['Clostridium Perfringens', 'Tuberculosis', 'Johne Disease', 'Anthrax', 'Brucellosis'],
        'Parasitic': ['Coccidia', 'Internal Worms', 'Liver Fluke', 'Lice', 'Meningeal Worm'],
        'Metabolic': ['Hepatic Lipidosis', 'Hypocalcemia', 'Ketosis', 'Copper Deficiency', 'Rickets'],
        'Respiratory': ['Pneumonia', 'Bronchitis', 'Influenza', 'Aspergillosis', 'Pleuropneumonia'],
        'Cardiovascular': ['Endocarditis', 'Pericarditis', 'Myocarditis', 'Valvular Disease', 'Arrhythmia'],
        'Musculoskeletal': ['Arthritis', 'Foot Rot', 'Laminitis', 'Fractures', 'White Muscle Disease'],
        'Gastrointestinal': ['Gastric Ulcers', 'Enterotoxemia', 'Acidosis', 'Diarrhea', 'Johne Disease']
    },
    'Fish': {
        'Viral': ['Viral Hemorrhagic Septicemia', 'Infectious Hematopoietic Necrosis', 'Spring Viremia Carp', 'Koi Herpesvirus', 'White Spot Syndrome'],
        'Bacterial': ['Aeromonas Infection', 'Edwardsiella', 'Vibriosis', 'Mycobacteriosis', 'Columnaris'],
        'Parasitic': ['Ichthyophthirius', 'Gyrodactylus', 'Dactylogyrus', 'Anchor Worm', 'Fish Lice'],
        'Metabolic': ['Fatty Liver', 'Swim Bladder Disorder', 'Dropsy', 'Malnutrition', 'Vitamin Deficiency'],
        'Respiratory': ['Gill Disease', 'Bacterial Gill Disease', 'Fungal Gill Infection', 'Branchiomycosis', 'Gill Hyperplasia'],
        'Cardiovascular': ['Cardiomyopathy', 'Pericarditis', 'Myocarditis', 'Heart Parasites', 'Septic Carditis'],
        'Musculoskeletal': ['Spinal Deformity', 'Fractures', 'Swim Bladder Issues', 'Fin Rot', 'Skeletal Anomalies'],
        'Gastrointestinal': ['Dropsy', 'Enteritis', 'Bloat', 'Constipation', 'Intestinal Blockage']
    }
}

def validate_prediction(animal, disease, category=None):
    """
    Validate if a disease is biologically plausible for given animal.
    
    Args:
        animal: Animal species
        disease: Predicted disease
        category: Disease category (optional)
        
    Returns:
        Dictionary with validation results
    """
    if animal not in ANIMAL_DISEASE_COMPATIBILITY:
        return {
            'is_biologically_plausible': False,
            'validation_reason': f'Unknown animal species: {animal}',
            'requires_veterinary_confirmation': True,
            'animal': animal,
            'disease': disease
        }
    
    # Check if disease exists for this animal
    animal_diseases = ANIMAL_DISEASE_COMPATIBILITY[animal]
    
    # Search across all categories for this animal
    found = False
    found_category = None
    
    for cat, diseases in animal_diseases.items():
        if disease in diseases:
            found = True
            found_category = cat
            break
    
    if found:
        # Check if category matches (if provided)
        category_match = True
        if category and found_category != category:
            category_match = False
            
        return {
            'is_biologically_plausible': True,
            'validation_reason': 'Compatible' if category_match else f'Disease found but in {found_category}, not {category}',
            'requires_veterinary_confirmation': not category_match,
            'animal': animal,
            'disease': disease,
            'category': found_category
        }
    else:
        return {
            'is_biologically_plausible': False,
            'validation_reason': f'{disease} is not documented for {animal}',
            'requires_veterinary_confirmation': True,
            'animal': animal,
            'disease': disease,
            'suggested_review': 'Consult specialist - unusual presentation'
        }

def get_alternative_diseases(animal, category, top_n=3):
    """
    Get alternative diseases for an animal in a specific category.
    
    Args:
        animal: Animal species
        category: Disease category
        top_n: Number of alternatives to return
        
    Returns:
        List of alternative diseases
    """
    if animal not in ANIMAL_DISEASE_COMPATIBILITY:
        return []
    
    animal_diseases = ANIMAL_DISEASE_COMPATIBILITY[animal]
    
    if category not in animal_diseases:
        # Return diseases from all categories
        all_diseases = []
        for diseases in animal_diseases.values():
            all_diseases.extend(diseases)
        return all_diseases[:top_n]
    
    return animal_diseases[category][:top_n]

def get_disease_prevalence(animal, disease):
    """
    Get prevalence information for a disease in an animal.
    (Based on veterinary epidemiological data)
    
    Args:
        animal: Animal species
        disease: Disease name
        
    Returns:
        Dictionary with prevalence information
    """
    # Comprehensive prevalence data based on research
    # Note: Expanded 20-species data handled by default fallback
    prevalence_data = {
        # Dogs
        'Canine Distemper': {'prevalence': 'Medium', 'severity': 'Fatal', 'urgency': 'Emergency'},
        'Canine Parvovirus': {'prevalence': 'Medium', 'severity': 'Fatal', 'urgency': 'Emergency'},
        'Rabies': {'prevalence': 'Low', 'severity': 'Fatal', 'urgency': 'Emergency'},
        'Canine Influenza': {'prevalence': 'Low', 'severity': 'Medium', 'urgency': 'Urgent'},
        'Kennel Cough': {'prevalence': 'High', 'severity': 'Low', 'urgency': 'Routine'},
        'Leptospirosis': {'prevalence': 'Low', 'severity': 'High', 'urgency': 'Urgent'},
        'Hip Dysplasia': {'prevalence': 'High', 'severity': 'Medium', 'urgency': 'Important'},
        'Diabetes Mellitus': {'prevalence': 'Medium', 'severity': 'High', 'urgency': 'Important'},
        
        # Cats
        'Feline Panleukopenia': {'prevalence': 'Medium', 'severity': 'Fatal', 'urgency': 'Emergency'},
        'Feline Leukemia Virus': {'prevalence': 'Medium', 'severity': 'Fatal', 'urgency': 'Urgent'},
        'Hypertrophic Cardiomyopathy': {'prevalence': 'High', 'severity': 'High', 'urgency': 'Urgent'},
        'Chronic Kidney Disease': {'prevalence': 'High', 'severity': 'High', 'urgency': 'Important'},
        'Hyperthyroidism': {'prevalence': 'High', 'severity': 'Medium', 'urgency': 'Important'},
        
        # Cattle
        'Bovine Viral Diarrhea': {'prevalence': 'High', 'severity': 'High', 'urgency': 'Urgent'},
        'Foot-and-Mouth Disease': {'prevalence': 'Low', 'severity': 'Fatal', 'urgency': 'Emergency'},
        'Mastitis': {'prevalence': 'Very High', 'severity': 'Medium', 'urgency': 'Important'},
        'Milk Fever': {'prevalence': 'Medium', 'severity': 'High', 'urgency': 'Urgent'},
        
        # Pigs
        'African Swine Fever': {'prevalence': 'Low', 'severity': 'Fatal', 'urgency': 'Emergency'},
        'PRRS': {'prevalence': 'High', 'severity': 'High', 'urgency': 'Urgent'},
        'Swine Erysipelas': {'prevalence': 'Medium', 'severity': 'Medium', 'urgency': 'Important'},
        
        # Sheep
        'Bluetongue': {'prevalence': 'Medium', 'severity': 'High', 'urgency': 'Urgent'},
        'Pregnancy Toxemia': {'prevalence': 'Medium', 'severity': 'Fatal', 'urgency': 'Emergency'},
        'Footrot': {'prevalence': 'High', 'severity': 'Medium', 'urgency': 'Important'},
        
        # Horses
        'Equine Influenza': {'prevalence': 'Medium', 'severity': 'Medium', 'urgency': 'Urgent'},
        'Laminitis': {'prevalence': 'Medium', 'severity': 'High', 'urgency': 'Emergency'},
        'Colic': {'prevalence': 'High', 'severity': 'High', 'urgency': 'Emergency'},
        'Strangles': {'prevalence': 'Medium', 'severity': 'Medium', 'urgency': 'Urgent'},
        
        # Goats
        'Caseous Lymphadenitis': {'prevalence': 'High', 'severity': 'Medium', 'urgency': 'Important'},
        'Haemonchus': {'prevalence': 'High', 'severity': 'High', 'urgency': 'Urgent'},
        
        # Chickens
        'Newcastle Disease': {'prevalence': 'Medium', 'severity': 'Fatal', 'urgency': 'Emergency'},
        'Coccidiosis': {'prevalence': 'Very High', 'severity': 'Medium', 'urgency': 'Important'},
        'Avian Influenza': {'prevalence': 'Low', 'severity': 'Fatal', 'urgency': 'Emergency'},
        
        # Common
        'Roundworm': {'prevalence': 'High', 'severity': 'Low', 'urgency': 'Routine'},
        'Hookworm': {'prevalence': 'Medium', 'severity': 'Medium', 'urgency': 'Important'},
        'Giardia': {'prevalence': 'High', 'severity': 'Low', 'urgency': 'Routine'},
        'E.coli Infection': {'prevalence': 'High', 'severity': 'Medium', 'urgency': 'Important'},
        'Salmonellosis': {'prevalence': 'Medium', 'severity': 'Medium', 'urgency': 'Important'},
        'Pneumonia': {'prevalence': 'High', 'severity': 'High', 'urgency': 'Urgent'},
        'Arthritis': {'prevalence': 'High', 'severity': 'Medium', 'urgency': 'Important'},
    }
    
    return prevalence_data.get(disease, {
        'prevalence': 'Unknown',
        'severity': 'Unknown',
        'urgency': 'Consult Veterinarian'
    })

def create_medical_disclaimer():
    """Generate medical disclaimer text."""
    return """
    ⚠️ MEDICAL DISCLAIMER ⚠️
    
    This AI system is intended for veterinary decision support only, not as a substitute 
    for professional veterinary judgment, diagnosis, or treatment.
    
    • Always consult with a qualified veterinarian for medical decisions
    • Laboratory confirmation may be required for definitive diagnosis
    • Treatment should not be initiated based solely on AI predictions
    • This system does not replace physical examination or medical history assessment
    • Emergency situations require immediate veterinary attention
    
    By using this system, you acknowledge these limitations and agree to use it 
    only as a supportive tool in conjunction with professional veterinary care.
    """

def get_all_supported_species():
    """Get list of all supported animal species"""
    return list(ANIMAL_DISEASE_COMPATIBILITY.keys())

def get_all_categories():
    """Get list of all disease categories"""
    return list(set(cat for animal in ANIMAL_DISEASE_COMPATIBILITY.values() for cat in animal.keys()))

def get_category_statistics():
    """Get statistics about the disease database"""
    stats = {
        'total_species': len(ANIMAL_DISEASE_COMPATIBILITY),
        'total_categories': len(get_all_categories()),
        'diseases_per_species': {},
        'total_unique_diseases': set()
    }
    
    for animal, categories in ANIMAL_DISEASE_COMPATIBILITY.items():
        total_diseases = sum(len(diseases) for diseases in categories.values())
        stats['diseases_per_species'][animal] = total_diseases
        for diseases in categories.values():
            stats['total_unique_diseases'].update(diseases)
    
    stats['total_diseases'] = len(stats['total_unique_diseases'])
    del stats['total_unique_diseases']  # Remove the set, keep the count
    
    return stats
