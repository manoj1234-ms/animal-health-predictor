"""
AI Specialist Chat Assistant
A context-aware chat interface for veterinarians and pet owners to discuss diagnoses with an AI specialist.
"""
import streamlit as st
import time
import random

# st.set_page_config is handled by app_dashboard.py

def get_specialist_response(user_input, context):
    """
    AI Specialist Logic with basic keyword detection for pseudo-intelligence.
    """
    user_input = user_input.lower()
    disease = context.get('disease', 'the condition')
    category = context.get('category', 'general health')
    treatment = context.get('treatment', {})
    
    if "medication" in user_input or "drug" in user_input or "medicine" in user_input:
        meds = ", ".join(treatment.get('medications', ['standard protocol meds']))
        return f"For {disease}, we typically prescribe: {meds}. Always verify dosages based on the patient's weight."
    
    if "prognosis" in user_input or "recovery" in user_input or "better" in user_input:
        prog = treatment.get('prognosis', 'guarded to fair')
        return f"The prognosis for {disease} is generally considered: {prog}. Early intervention is key."
    
    if "treatment" in user_input or "plan" in user_input:
        plan = treatment.get('treatment_plan', 'standard supportive care')
        return f"The recommended plan for {disease} includes: {plan}. Monitor vitals every 4 hours."

    responses = [
        f"Based on the {category} markers we're seeing for {disease}, I recommend sticking to the established protocols.",
        f"The symptoms for {disease} can be complex. Have you observed any changes in the patient's respiratory rate?",
        f"In my experience with {category} cases, {disease} requires strict hydration management. How is the skin turgor?",
        f"I've updated the digital referral for this {disease} case. You can coordinate with the specialists on the 'Find Care' tab.",
        "That's a specific clinical question. I suggest cross-referencing with the latest veterinary journals for this species."
    ]
    return random.choice(responses)

st.title("💬 VetNet AI Specialist Chat")
st.markdown("Consult with our simulated AI specialists about your diagnosis and treatment plan.")

# --- Context Setup ---
# We use session state to pass context from the Intake form
if 'last_diagnosis' not in st.session_state:
    st.session_state.last_diagnosis = {"disease": "Unspecified", "category": "General"}

context = st.session_state.last_diagnosis

with st.sidebar:
    st.subheader("Case Context")
    st.info(f"**Patient:** {context.get('animal', 'Unknown')}\n\n**Diagnosis:** {context.get('disease')}\n\n**Category:** {context.get('category')}")
    if st.button("Clear Chat"):
        st.session_state.messages = []

# --- Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"Hello! I am your AI Specialist for **{context.get('category')}**. I see we are dealing with a potential case of **{context.get('disease')}**. How can I assist you with the treatment plan today?"}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask the specialist about treatment, dosage, or follow-up..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = get_specialist_response(prompt, context)
        
        # Simulate typing effect
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
