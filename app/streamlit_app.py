"""Minimal Streamlit entrypoint for the MVP demo."""

import streamlit as st


st.set_page_config(page_title="Elderly Symptom Reasoning Assistant", page_icon=":stethoscope:")

st.title("Elderly Symptom Reasoning Assistant")
st.caption("Initial MVP scaffold for CS3263.")

user_input = st.text_area(
    "Describe the symptoms",
    placeholder="Example: I feel tired, slightly dizzy, and have a dry mouth.",
)

if st.button("Analyze"):
    if not user_input.strip():
        st.warning("Please enter a symptom description.")
    else:
        st.info("The end-to-end reasoning pipeline has not been wired up yet.")

st.markdown(
    """
    ### Planned output

    - Extracted evidence variables
    - Ranked condition probabilities
    - Emergency override warning when triggered
    - Short explanation and safe next-step guidance
    """
)
