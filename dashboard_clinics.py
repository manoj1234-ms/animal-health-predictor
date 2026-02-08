"""
Clinic & Specialist Locator Dashboard
AI-powered referral system to find the best care for diagnosed conditions.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from src.specialist_network import CLINIC_DB, DISEASE_TO_SPECIALTY, get_specialists_for_disease
import os

# st.set_page_config is already handled by app_dashboard.py

st.title("📍 AI Clinic & Specialist Network")
st.markdown("Find the best-rated veterinary specialists based on AI diagnosis results.")

# --- Filters ---
col_f1, col_f2 = st.columns([1, 2])

with col_f1:
    st.subheader("Search Filters")
    countries = sorted(list(set([c.get("country", "USA") for c in CLINIC_DB])))
    selected_country = st.selectbox("Select Country", ["All"] + countries)
    
    # Filter states based on country
    if selected_country != "All":
        states = sorted(list(set([c.get("state") for c in CLINIC_DB if c.get("country") == selected_country and c.get("state") is not None])))
        selected_state = st.selectbox("Select State/Province", ["All"] + states)
    else:
        selected_state = "All"
        
    # Filter cities based on state
    if selected_state != "All":
        cities = sorted(list(set([c.get("city") for c in CLINIC_DB if c.get("state") == selected_state and c.get("city") is not None])))
        selected_city = st.selectbox("Select City", ["All"] + cities)
    else:
        selected_city = "All"
    
    all_specialties = sorted(list(set([s for c in CLINIC_DB for s in c["specialties"]])))
    selected_spec = st.multiselect("Filter by Specialty", all_specialties)
    
    show_emergency = st.toggle("Only Show Emergency Clinics")
    min_rating = st.slider("Min Rating", 3.0, 5.0, 4.0)

# --- AI Recommender Section ---
st.info("💡 **AI Tip:** Selecting a disease category will automatically highlight the most relevant specialists.")
ai_category = st.selectbox("Simulate AI Diagnosis Category", ["-"] + list(DISEASE_TO_SPECIALTY.keys()))

# --- Map View ---
st.subheader("Clinic Locator")

# Convert DB to DataFrame for mapping
df_clinics = pd.DataFrame(CLINIC_DB)
if 'country' not in df_clinics.columns:
    df_clinics['country'] = 'USA'

# Filter Logic
filtered_df = df_clinics.copy()

if selected_country != "All":
    filtered_df = filtered_df[filtered_df['country'] == selected_country]
if selected_state != "All":
    filtered_df = filtered_df[filtered_df['state'] == selected_state]
if selected_city != "All":
    filtered_df = filtered_df[filtered_df['city'] == selected_city]
if selected_spec:
    filtered_df = filtered_df[filtered_df['specialties'].apply(lambda specs: any(s in selected_spec for s in specs))]
if show_emergency:
    filtered_df = filtered_df[filtered_df['emergency'] == True]
filtered_df = filtered_df[filtered_df['rating'] >= min_rating]

# AI Filtering (Overwrites if selected)
if ai_category != "-":
    needed = DISEASE_TO_SPECIALTY[ai_category]
    filtered_df = filtered_df[filtered_df['specialties'].apply(lambda specs: any(s in needed for s in specs))]
    st.success(f"Showing specialists for **{ai_category}** conditions.")

if not filtered_df.empty:
    # Auto-zoom based on selection
    if selected_city != "All":
        zoom_level = 14
    elif selected_state != "All":
        zoom_level = 8
    elif selected_country != "All":
        zoom_level = 5
    else:
        zoom_level = 1
    
    fig = px.scatter_mapbox(
        filtered_df,
        lat="lat",
        lon="lon",
        hover_name="name",
        hover_data=["specialties", "rating", "contact", "city", "state", "country"],
        color="emergency",
        color_discrete_map={True: "red", False: "blue"},
        size_max=15,
        zoom=zoom_level,
        height=500
    )
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True, key="clinic_map")
else:
    st.warning("No clinics match your filters.")

# --- Clinic List ---
st.subheader("Clinic Directory")
for _, clinic in filtered_df.iterrows():
    with st.container():
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            st.markdown(f"### {clinic['name']}")
            st.markdown(f"📍 **Location:** {clinic.get('city', 'N/A')}, {clinic.get('state', 'N/A')}, {clinic.get('country', 'N/A')}")
            st.markdown(f"**Specialties:** {', '.join(clinic['specialties'])}")
            st.markdown(f"**Doctors:** {', '.join(clinic['doctors'])}")
        with c2:
            st.metric("Rating", f"{clinic['rating']}⭐")
            if clinic['emergency']:
                st.error("🚨 Emergency")
        with c3:
            st.button("☎️ Contact", key=f"call_{clinic['id']}")
            st.button("📄 Book Ink", key=f"book_{clinic['id']}")
        st.divider()

st.caption("Map data simulated for demonstration. Clinic availability subject to change.")
