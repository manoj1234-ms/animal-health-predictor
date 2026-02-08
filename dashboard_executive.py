"""
Executive Dashboard (KPIs & High-Level Metrics)
Focus on Business Impact and Overall System Adoption.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from src.monitoring import SystemMonitor

# st.set_page_config(layout="wide", page_title="VetNet Executive View")

# Load Logs
monitor = SystemMonitor()
logs_df = monitor.get_recent_predictions(limit=1000)

if logs_df.empty:
    st.warning("Data pending. Executive overview will populate shortly.")
    st.stop()
    
# --- KPI Row ---
st.title("📊 Executive Dashboard")
st.markdown("High-level overview of VetNet adoption and performance.")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_predictions = len(logs_df)
# Simulated "Adoption" - unique animals ~= unique patients
unique_patients = logs_df.groupby(['animal', 'category']).ngroups
avg_diagnosis_time = logs_df['latency_ms'].mean() / 1000 # seconds
# Assuming saved time per diagnosis vs manual
time_saved_hours = (total_predictions * 15 * 60) / 3600 # 15 mins saved per case

kpi1.metric("Total Diagnoses Run", f"{total_predictions:,}", delta="Today")
kpi2.metric("Unique Patient Scenarios", f"{unique_patients}")
kpi3.metric("Avg AI Response Time", f"{avg_diagnosis_time:.3f} s", delta="-99% vs Manual")
kpi4.metric("Est. Vet Hours Saved", f"{time_saved_hours:.1f} hrs", delta="YTD")

# --- Trends & Forecast ---
t1, t2 = st.columns(2)

with t1:
    st.subheader("Daily Usage Forecast")
    # Simulate trend
    dates = pd.date_range(end=pd.Timestamp.now(), periods=30)
    usage = np.random.randint(50, 200, size=30).cumsum()
    forecast = np.poly1d(np.polyfit(range(30), usage, 1))(range(30, 40))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=usage, mode='lines', name='Actual'))
    fig.add_trace(go.Scatter(x=pd.date_range(start=pd.Timestamp.now(), periods=10), y=forecast, mode='lines', name='Forecast', line=dict(dash='dash')))
    st.plotly_chart(fig, key="usage_forecast_chart", **{'use_container_width': True} if st.__version__ < "1.40.0" else {'width': "stretch"})

with t2:
    st.subheader("Diagnosis Category Share")
    # Pie chart of Categories
    if not logs_df.empty:
        fig_pie = go.Figure(data=[go.Pie(labels=logs_df['category'].value_counts().index, values=logs_df['category'].value_counts().values, hole=.3)])
        st.plotly_chart(fig_pie, key="cat_share_pie_chart", **{'use_container_width': True} if st.__version__ < "1.40.0" else {'width': "stretch"})
        
# --- ROI Calculator ---
st.markdown("---")
st.header("ROI Calculator")

c1, c2, c3 = st.columns(3)
vet_hourly_rate = c1.number_input("Vet Hourly Rate ($)", value=100)
cases_per_day = c2.number_input("Avg Cases / Day", value=20)
mins_saved = c3.number_input("Mins Saved / Case", value=15)

daily_savings = (cases_per_day * mins_saved / 60) * vet_hourly_rate
monthly_savings = daily_savings * 22 # working days
annual_savings = monthly_savings * 12

st.success(f"Projected Annual Savings: **${annual_savings:,.2f}** per clinic")
