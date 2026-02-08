"""
Admin Dashboard for Veterinary AI System
Real-time monitoring of model performance and system health.
"""
import streamlit as st
import pandas as pd
import json
import time
from src.monitoring import SystemMonitor
import plotly.express as px
import plotly.graph_objects as go

# Config
# st.set_page_config(
#     page_title="VetNet Admin Dashboard",
#     page_icon="🐾",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 10px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #FFFFFF;
    }
    .metric-label {
        color: #AAAAAA;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

monitor = SystemMonitor()

def load_data():
    df_preds = monitor.get_recent_predictions(limit=500)
    df_metrics = monitor.get_system_metrics(limit=100)
    return df_preds, df_metrics

# Sidebar
st.sidebar.title("🐾 VetNet Admin")
st.sidebar.markdown("---")
refresh_rate = st.sidebar.slider("Refresh Rate (s)", 1, 60, 5)
st.sidebar.markdown("### System Status")
st.sidebar.success("● API Online")
st.sidebar.success("● Model Loaded (VetNet)")

# Main Layout
st.title("Veterinary AI Command Center")
st.markdown("Real-time monitoring of disease prediction system")

# Auto-refresh loop
placeholder = st.empty()

while True:
    with placeholder.container():
        df_preds, df_metrics = load_data()
        
        # --- Top Metrics Row ---
        col1, col2, col3, col4 = st.columns(4)
        
        total_preds = len(df_preds) if not df_preds.empty else 0
        avg_latency = df_preds['latency_ms'].mean() if not df_preds.empty else 0
        error_rate = (len(df_preds[df_preds['status'] == 'error']) / total_preds * 100) if total_preds > 0 else 0
        avg_conf = df_preds['disease_confidence'].mean() * 100 if not df_preds.empty else 0
        
        with col1:
            st.metric("Total Predictions (24h)", f"{total_preds}", delta="Live")
        with col2:
            st.metric("Avg Latency", f"{avg_latency:.1f} ms", delta_color="inverse")
        with col3:
            st.metric("Error Rate", f"{error_rate:.1f}%", delta_color="inverse")
        with col4:
            st.metric("Avg Confidence", f"{avg_conf:.1f}%")
            
        # --- Charts Row 1 ---
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.subheader("Category Distribution")
            if not df_preds.empty and 'category' in df_preds.columns:
                cat_counts = df_preds['category'].value_counts()
                fig_cat = px.pie(values=cat_counts.values, names=cat_counts.index, hole=0.4)
                fig_cat.update_layout(margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig_cat, key=f"cat_dist_chart_{time.time()}", **{'use_container_width': True} if st.__version__ < "1.40.0" else {'width': "stretch"})
            else:
                st.info("No prediction data yet.")
                
        with col_c2:
            st.subheader("System Health (CPU/RAM)")
            if not df_metrics.empty:
                fig_sys = go.Figure()
                fig_sys.add_trace(go.Scatter(y=df_metrics['cpu_percent'], name='CPU %', line=dict(color='#FF4B4B')))
                fig_sys.add_trace(go.Scatter(y=df_metrics['memory_percent'], name='Memory %', line=dict(color='#4CAF50')))
                fig_sys.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
                st.plotly_chart(fig_sys, key=f"sys_health_chart_{time.time()}", **{'use_container_width': True} if st.__version__ < "1.40.0" else {'width': "stretch"})
            else:
                st.info("No system metrics yet.")

        # --- Recent Logs Table ---
        st.subheader("Recent Predictions")
        if not df_preds.empty:
            display_cols = ['timestamp', 'animal', 'category', 'disease', 'disease_confidence', 'latency_ms', 'status']
            st.dataframe(df_preds[display_cols].sort_values('timestamp', ascending=False).head(10), use_container_width=True)
        
    time.sleep(refresh_rate)
