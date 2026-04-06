"""Minimal Streamlit entrypoint for the MVP demo."""

from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.parser import parse_free_text
from src.rules import evaluate_overrides


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
        evidence = parse_free_text(user_input)
        extracted = {key: value for key, value in evidence.items() if value != "unknown"}
        override = evaluate_overrides(evidence)

        st.subheader("Extracted Evidence")
        if extracted:
            st.json(extracted)
        else:
            st.caption("No symptom phrases were recognized yet.")

        st.subheader("Safety Override")
        if bool(override["triggered"]):
            st.error(str(override["message"]))
            st.caption(f"Triggered rule: {override['rule_id']}")
        else:
            st.success("No urgent override triggered from the currently recognized evidence.")

        st.info("Parser and safety checkpoints are active. Bayesian ranking is the next slice.")

st.markdown(
    """
    ### Planned output

    - Extracted evidence variables
    - Ranked condition probabilities
    - Emergency override warning when triggered
    - Short explanation and safe next-step guidance
    """
)
