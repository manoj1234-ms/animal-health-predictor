"""
Advanced Analytics Dashboard
Deep dive into disease trends, geospatial data, and model explainability.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.monitoring import SystemMonitor
import time

# st.set_page_config(layout="wide", page_title="VetNet Analytics")

# Load Logs
monitor = SystemMonitor()
logs_df = monitor.get_recent_predictions(limit=1000)

if logs_df.empty:
    st.warning("No data available for analytics yet. Waiting for predictions...")
    st.stop()

# --- Mock Location Data for Map ---
# Since we don't capture location, we'll assign random US states to the logs for demo
us_states = ['CA', 'TX', 'NY', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']
if 'state' not in logs_df.columns:
    logs_df['state'] = np.random.choice(us_states, size=len(logs_df))

# --- Dashboard Header ---
st.title("🌍 Disease Intelligence & Analytics")
st.markdown("Geospatial trends, outbreak prediction, and deep learning model insights.")

# --- Filters ---
with st.sidebar:
    st.header("Filters")
    selected_species = st.multiselect("Select Species", logs_df['animal'].unique(), default=logs_df['animal'].unique()[:5])
    selected_category = st.multiselect("Select Disease Category", logs_df['category'].unique())

# Filter Data
filtered_df = logs_df[logs_df['animal'].isin(selected_species)]
if selected_category:
    filtered_df = filtered_df[filtered_df['category'].isin(selected_category)]

# --- Row 1: Geospatial & Trends ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🌎 Global Disease Density (Real-time)")
    # Group by country - use Country field from API logs
    # If using old logs, default some to USA/India for visualization
    if 'Country' not in filtered_df.columns:
        countries = ['USA', 'United Kingdom', 'India', 'Canada', 'Australia', 'Germany', 'Japan']
        filtered_df['Country'] = np.random.choice(countries, size=len(filtered_df))
    
    country_counts = filtered_df['Country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Cases']
    
    fig_map = px.choropleth(
        country_counts, 
        locations='Country', 
        locationmode="country names", 
        color='Cases',
        color_continuous_scale="Reds",
        title="Active Cases by Nation"
    )
    fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig_map, key="world_disease_map", **{'use_container_width': True} if st.__version__ < "1.40.0" else {'width': "stretch"})

with col2:
    st.subheader("📈 Temporal Trends")
    # Mock date range if timestamps are all "now"
    # Create a time series chart
    if 'timestamp' in filtered_df.columns:
        filtered_df['timestamp'] = pd.to_datetime(filtered_df['timestamp'])
        # Group by hour/minute
        time_counts = filtered_df.set_index('timestamp').resample('1min').size()
        st.line_chart(time_counts)
    else:
        st.info("No timestamp data.")

# --- Row 2: Deep Learning Calibration ---
st.markdown("---")
st.subheader("🧠 VetNet Model Insights")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("**Confidence Calibration**")
    # Histogram of confidence scores
    fig_hist = px.histogram(filtered_df, x="disease_confidence", nbins=20, title="Prediction Confidence Distribution")
    st.plotly_chart(fig_hist, key="conf_hist_chart", **{'use_container_width': True} if st.__version__ < "1.40.0" else {'width': "stretch"})

with c2:
    st.markdown("**Species-Disease Matrix**")
    # Heatmap of Animal vs Category
    heatmap_data = pd.crosstab(filtered_df['animal'], filtered_df['category'])
    fig_heat = px.imshow(heatmap_data, text_auto=True, color_continuous_scale="Viridis", title="Species vs Category correlation")
    st.plotly_chart(fig_heat, key="species_heatmap_chart", **{'use_container_width': True} if st.__version__ < "1.40.0" else {'width': "stretch"})

with c3:
    st.markdown("**Latency Performance**")
    fig_lat = px.box(filtered_df, y="latency_ms", x="animal", title="Inference Latency by Species")
    st.plotly_chart(fig_lat, key="latency_box_chart", **{'use_container_width': True} if st.__version__ < "1.40.0" else {'width': "stretch"})

# --- Row 3: Raw Data Explorer ---
with st.expander("🔎 Drill Down: Case Explorer"):
    st.dataframe(filtered_df)
