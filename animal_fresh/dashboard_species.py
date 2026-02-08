"""
Species Analytics Dashboard
Deep dive into species-specific health trends.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from src.monitoring import SystemMonitor

# st.set_page_config(layout="wide", page_title="VetNet Species Analytics")

monitor = SystemMonitor()
logs_df = monitor.get_recent_predictions(limit=1000)

if logs_df.empty:
    st.warning("No data available.")
    st.stop()

st.title("🐾 Species Analytics")

# --- Species Selector ---
species_list = logs_df['animal'].unique()
selected_species = st.selectbox("Select Species", species_list)

# Filter Data
species_df = logs_df[logs_df['animal'] == selected_species]

col1, col2 = st.columns(2)

with col1:
    st.metric(f"Total {selected_species} Cases", len(species_df))
    
    # Top Diseases
    top_diseases = species_df['disease'].value_counts().head(5)
    st.subheader(f"Most Common Diseases in {selected_species}")
    st.bar_chart(top_diseases)

with col2:
    st.metric("Avg Confidence", f"{species_df['disease_confidence'].mean()*100:.1f}%")
    
    # Category Distribution
    st.subheader(f"Disease Categories in {selected_species}")
    fig = px.pie(species_df, names='category', title=f"{selected_species} Health Profile")
    st.plotly_chart(fig, key="species_pie_chart", **{'use_container_width': True} if st.__version__ < "1.40.0" else {'width': "stretch"})

# --- Age Analysis ---
st.subheader("Age Vulnerability Analysis")
# Determine age brackets if age is available in logs? 
# Logs currently save summary. We might need detailed logs if we captured age.
# `monitoring.py` only saves minimal info.
# For Phase 3, let's assume we want to improve monitoring to capture Age.

st.info("Detailed age demographics coming in next update.")
