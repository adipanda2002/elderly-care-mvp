"""Minimal Streamlit entrypoint for the MVP demo."""

from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.bn import rank_conditions
from src.explain import build_response
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
        condition_scores = rank_conditions(evidence)
        response = build_response(evidence, condition_scores, override)

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

        st.subheader("Condition Ranking")
        ranking_rows = [
            {
                "condition": str(condition["label"]),
                "probability": f"{float(condition['probability']) * 100:.1f}%",
            }
            for condition in response["conditions"]
        ]
        st.table(ranking_rows)

        if bool(override["triggered"]):
            st.caption("Urgent escalation takes precedence over the ranked conditions shown above.")

        st.subheader("Explanation")
        st.write(str(response["explanation"]))

        st.subheader("Recommendation")
        st.write(str(response["recommendation"]))

        st.caption(str(response["disclaimer"]))

st.markdown(
    """
    ### Planned output

    - Extracted evidence variables
    - Ranked condition probabilities
    - Emergency override warning when triggered
    - Short explanation and safe next-step guidance
    """
)
