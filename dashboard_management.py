import streamlit as st
import pandas as pd
import os
from src.data_manager import validate_csv, save_custom_data, merge_and_retrain, REQUIRED_COLUMNS

st.title("📂 Data Management & AI Retraining")
st.markdown("""
Use this portal to upload real hospital records and retrain our AI specialists. 
This ensures the system stays accurate as new disease strains emerge or local conditions change.
""")

# --- Step 1: Bulk Upload ---
st.header("1. Bulk Upload Hospital Records")
st.info(f"Please ensure your CSV contains the following columns: {', '.join(REQUIRED_COLUMNS)}")

template_df = pd.DataFrame(columns=REQUIRED_COLUMNS)
st.download_button(
    label="⬇️ Download CSV Template",
    data=template_df.to_csv(index=False),
    file_name="vetnet_data_template.csv",
    mime="text/csv"
)

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("📊 Data Preview (Top 5 Rows):")
    st.dataframe(df.head())
    
    is_valid, missing = validate_csv(df)
    if is_valid:
        if st.button("✅ Import Records to Database"):
            save_custom_data(df)
            st.success(f"Successfully imported {len(df)} records!")
    else:
        st.error(f"Invalid CSV structure. Missing columns: {', '.join(missing)}")

# --- Step 2: System Retraining ---
st.divider()
st.header("2. AI Model Retraining")
st.warning("⚠️ Retraining will take several minutes. The system will be updated with the latest insights from your combined dataset.")

if st.button("🚀 Start Deep Learning Retraining", type="primary"):
    with st.spinner("Merging datasets and retraining Neural Network... This may take a moment."):
        success, message = merge_and_retrain()
        if success:
            st.success(message)
            st.balloons()
        else:
            st.error(message)

# --- Statistics ---
st.divider()
st.subheader("📈 Database Statistics")
if os.path.exists('data/custom_records.csv'):
    df_custom = pd.read_csv('data/custom_records.csv')
    st.write(f"**Custom Records Contributed:** {len(df_custom)}")
    st.write(f"**Species Represented:** {df_custom['Animal'].nunique()}")
else:
    st.write("No custom records have been uploaded yet. The system is currently running on the core expanded dataset (15,000 samples).")
