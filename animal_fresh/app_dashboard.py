"""
Unified Dashboard Launcher (VetNet AI Suite)
Combines Admin, Analytics, and Executive views into a single Streamlit App.
"""
import streamlit as st
import sys
import os

# Page Config MUST be the first command
st.set_page_config(page_title="VetNet AI Suite", layout="wide", page_icon="🐾")

st.sidebar.title("🐾 VetNet Navigation")

# Initialize selection in session state if not present
if 'selection' not in st.session_state:
    st.session_state.selection = "Patient Intake"

selection = st.sidebar.radio("Go to:", 
    ["Patient Intake", "Find Care", "Specialist Chat", "Admin Dashboard", "Analytics Hub", "Species Analytics", "Executive View"],
    index=["Patient Intake", "Find Care", "Specialist Chat", "Admin Dashboard", "Analytics Hub", "Species Analytics", "Executive View"].index(st.session_state.selection),
    key="nav_radio"
)

# Update selection globally
st.session_state.selection = selection

import importlib.util

def run_module(module_path):
    # This is a hack to run another streamlit script inside this one
    # It might have issues with duplicate widgets ID if not careful
    try:
        with open(module_path, encoding='utf-8') as f:
            code = f.read()
            # Remove set_page_config from code to avoid error
            code = code.replace("st.set_page_config", "# st.set_page_config")
            exec(code, globals())
    except FileNotFoundError:
        st.error(f"Module not found: {module_path}")

base_dir = os.path.dirname(os.path.abspath(__file__))

if selection == "Patient Intake":
    run_module(os.path.join(base_dir, "dashboard_clinician.py"))

elif selection == "Find Care":
    run_module(os.path.join(base_dir, "dashboard_clinics.py"))

elif selection == "Specialist Chat":
    run_module(os.path.join(base_dir, "dashboard_chat.py"))

elif selection == "Admin Dashboard":
    run_module(os.path.join(base_dir, "dashboard_admin.py"))

elif selection == "Analytics Hub":
    run_module(os.path.join(base_dir, "dashboard_analytics.py"))

elif selection == "Species Analytics":
    run_module(os.path.join(base_dir, "dashboard_species.py"))

elif selection == "Executive View":
    run_module(os.path.join(base_dir, "dashboard_executive.py"))
