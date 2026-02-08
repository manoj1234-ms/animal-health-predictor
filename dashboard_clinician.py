"""
Clinician Dashboard - VetNet
Interface for Veterinarians to input patient data and get disease predictions.
"""
import streamlit as st
import requests
import json
import pandas as pd
import time

# Verify API Connection
API_URL = "http://localhost:8000"

def get_prediction(data):
    try:
        response = requests.post(f"{API_URL}/predict", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error {response.status_code}: {response.text}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to backend API. Is it running?"}

# --- UI Layout ---
st.title("🩺 VetNet Clinician Portal")
st.markdown("### AI-Powered Disease Diagnosis Assistant")

# --- Document Intelligence ---
with st.expander("📄 Smart Document Intake (BETA)", expanded=False):
    st.markdown("Upload a veterinary lab report (PDF) to auto-fill the clinical data.")
    uploaded_doc = st.file_uploader("Upload Lab Report", type=["pdf"])
    
    if uploaded_doc is not None:
        from src.document_processor import extract_text_from_file, parse_animal_report
        with st.spinner("Extracting intelligence from document..."):
            raw_text = extract_text_from_file(uploaded_doc)
            extracted_data = parse_animal_report(raw_text)
            st.session_state.extracted_data = extracted_data
            st.success("Data extracted successfully! Review the form below.")
            with st.expander("View Raw Extracted Text"):
                st.text(raw_text)

# Initialize defaults from extracted data
ext = st.session_state.get('extracted_data', {})

# --- Patient Intake Form ---
with st.form("patient_intake_form"):
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Patient Details")
        animal_list = ["Dog", "Cat", "Horse", "Cow", "Pig", "Sheep", "Goat", "Chicken", "Turkey", "Duck", "Goose", "Rabbit", "Ferret", "Hamster", "Guinea Pig", "Rat", "Mouse", "Chinchilla", "Hedgehog", "Reptile (Generic)"]
        default_animal = ext.get('Animal', 'Dog')
        if default_animal not in animal_list: default_animal = 'Dog'
        
        animal_type = st.selectbox("Species", animal_list, index=animal_list.index(default_animal))
        country = st.selectbox("Region / Country", ["USA", "United Kingdom", "India", "Canada", "Australia", "Germany", "France", "Japan", "Brazil", "South Africa", "Other"])
        
        # New: Hyper-local fields
        c1_loc, c2_loc = st.columns(2)
        with c1_loc:
            state = st.text_input("State / Province", "California")
        with c2_loc:
            city = st.text_input("City / District", "Los Angeles")
            
        breed = st.text_input("Breed (Optional)", "Unknown")
        age = st.number_input("Age (Years)", 0.1, 30.0, float(ext.get('Age', 5.0)))
        weight = st.number_input("Weight (kg)", 0.1, 1000.0, 20.0)
        temp = st.number_input("Body Temperature (°C)", 30.0, 45.0, 38.5)
    
    with c2:
        st.subheader("Clinical Signs & Vitals")
        symptom_options = [
            "Vomiting", "Diarrhea", "Lethargy", "Fever", "Coughing", 
            "Sneezing", "Weight Loss", "Appetite Loss", "Lameness", 
            "Seizures", "Skin Lesions", "Hair Loss", "Abdominal Pain",
            "Dehydration", "Pale Gums", "Rapid Breathing", "Nasal Discharge"
        ]
        default_symptoms = ext.get('Symptoms', [])
        symptoms = st.multiselect("Observed Symptoms", symptom_options, default=[s for s in default_symptoms if s in symptom_options])
        
        st.markdown("**Blood Work (if available)**")
        wbc = st.number_input("WBC (10^9/L)", 0.0, 100.0, float(ext.get('WBC', 10.0)))
        rbc = st.number_input("RBC (10^12/L)", 0.0, 15.0, float(ext.get('RBC', 6.5)))
        pcv = st.number_input("PCV (%)", 0.0, 80.0, 40.0)
        
        # Extra fields often in reports
        hg = ext.get('Hemoglobin', 14.0)
        plt = ext.get('Platelets', 300.0)
        glu = ext.get('Glucose', 100.0)
        
    submitted = st.form_submit_button("Run AI Diagnosis", use_container_width=True)

if submitted:
    with st.spinner("Analyzing patient vitals..."):
        # Construct Payload
        # Mapping simple inputs to model features (simplified for demo)
        # Construct Payload matching simple_api.py PredictionRequest model
        # Note: Keys must match the Pydantic model exactly (Capitalized)
        patient_data = {
            "Animal": animal_type,
            "Country": country,
            "State": state,
            "City": city,
            "Age": float(age),
            "Gender": "Unknown", # Default as not in form
            "Breed": breed,
            "WBC": float(wbc),
            "RBC": float(rbc),
            "Hemoglobin": float(hg),
            "Platelets": float(plt),
            "Glucose": float(glu),
            "ALT": float(ext.get('ALT', 40.0)),
            "AST": float(ext.get('AST', 40.0)),
            "Urea": float(ext.get('Urea', 25.0)),
            "Creatinine": float(ext.get('Creatinine', 1.0)),
            "Symptom_Fever": 1 if "Fever" in symptoms else 0,
            "Symptom_Lethargy": 1 if "Lethargy" in symptoms else 0,
            "Symptom_Vomiting": 1 if "Vomiting" in symptoms else 0,
            "Symptom_Diarrhea": 1 if "Diarrhea" in symptoms else 0,
            "Symptom_WeightLoss": 1 if "Weight Loss" in symptoms else 0,
            "Symptom_SkinLesion": 1 if "Skin Lesions" in symptoms else 0,
            "Symptom_Coughing": 1 if "Coughing" in symptoms else 0,
            "Symptom_Lameness": 1 if "Lameness" in symptoms else 0
        }
        
        # Add defaults for missing numeric features expected by VetNet
        # (The model expects specific feature names, we fill them with averages if not in form)
        # Note: Ideally the API handles missing fields or we build a full form.
        # For this demo, we'll let the API/Model handle valid inputs.
        
        # Call API
        result = get_prediction(patient_data)
        
        time.sleep(0.5) # UI sugar
        
    if "error" in result:
        st.error(result["error"])
    else:
        # Save to session state for the Chat system
        st.session_state.last_diagnosis = {
            "animal": animal_type,
            "disease": result.get('predicted_disease'),
            "category": result.get('predicted_category'),
            "treatment": result.get('treatment')
        }
        
        # Success Display
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            st.success(f"## {result.get('predicted_disease', 'Unknown')}")
            conf = result.get('disease_confidence', 0) * 100
            st.metric("AI Confidence", f"{conf:.1f}%")
            st.info(f"Category: **{result.get('predicted_category', 'General')}**")
            
            # --- Chat Shortcut ---
            if st.button("💬 Open AI Specialist Chat", use_container_width=True):
                st.session_state.selection = "Specialist Chat"
                st.rerun()
            
        with res_col2:
            st.subheader("Recommended Treatment Plan")
            treatment = result.get('treatment', {})
            
            if treatment:
                st.markdown(f"**Plan:** {treatment.get('treatment_plan', 'Consult specialist.')}")
                st.markdown(f"**Medications:** {', '.join(treatment.get('medications', []))}")
                st.markdown(f"**Prognosis:** {treatment.get('prognosis', 'N/A')}")
                
                with st.expander("Follow-up Instructions"):
                    st.write(treatment.get('follow_up', 'Monitor closely.'))
            else:
                st.warning("No specific treatment protocol found in database.")

        # --- AI Referral Section ---
        st.markdown("---")
        st.subheader("📍 AI-Recommended Specialist Referral")
        from src.specialist_network import get_specialists_for_disease
        
        category = result.get('predicted_category', 'General')
        specialists = get_specialists_for_disease(category)
        
        if specialists:
            st.markdown(f"The AI has identified **{len(specialists)}** specialists nearby specialized in **{category}** conditions:")
            cols = st.columns(len(specialists[:3])) # Show top 3
            for i, spec in enumerate(specialists[:3]):
                with cols[i]:
                    st.info(f"**{spec['name']}**\n\nRating: {spec['rating']}⭐\n\n{spec['contact']}")
            
            if st.button("View All Nearby Clinics on Map"):
                st.session_state.selection = "Find Care" # Redirect logic if supported
                st.info("Please select 'Find Care' from the sidebar to view the full interactive map.")
        else:
            st.info("No highly specialized clinics found for this specific category nearby. Consulting a General Hospital is recommended.")

        # Disclaimer
        st.caption("⚠️ AI predictions are for decision support only. Always verify with clinical judgment.")
