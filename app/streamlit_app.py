"""Minimal Streamlit entrypoint for the MVP demo."""

from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.bn import rank_conditions
from src.eval import load_benchmark_summary
from src.explain import build_response
from src.parser import parse_free_text
from src.rules import evaluate_overrides


st.set_page_config(page_title="Elderly Symptom Reasoning Assistant", page_icon=":stethoscope:")

st.title("Elderly Symptom Reasoning Assistant")
st.caption("Initial MVP scaffold for CS3263.")

show_demo_notes = st.sidebar.checkbox("Show demo notes", value=True)

if show_demo_notes:
    benchmark_summary = load_benchmark_summary()

    st.sidebar.markdown("## Demo Notes")
    st.sidebar.caption(
        "Presentation-only notes for explaining the backend design. "
        "These would not be shown in a real end-user deployment."
    )

    with st.sidebar.expander("1. Symptom Parser", expanded=True):
        st.markdown(
            """
            - Free-text input is matched against a YAML-backed phrase lexicon in `config/symptom_lexicon.yaml`.
            - The parser supports simple synonym coverage and basic negation handling such as `no fever`.
            - Output is a fixed evidence schema with `yes`, `no`, or `unknown`.
            """
        )

    with st.sidebar.expander("2. Safety Override Layer"):
        st.markdown(
            """
            - Urgent red flags are checked with deterministic rules from `config/safety_rules.yaml`.
            - Rules take precedence over probabilistic ranking.
            - Examples include chest pain, fainting, severe confusion, and dizziness after a fall.
            """
        )

    with st.sidebar.expander("3. Bayesian Ranking Layer"):
        st.markdown(
            """
            - Condition ranking uses YAML-backed priors and evidence likelihoods from `config/cpts/`.
            - The current MVP scores the four modeled conditions and normalizes the posterior probabilities.
            - This keeps the model small, interpretable, and easy to justify in the report.
            """
        )

    with st.sidebar.expander("4. Explanation Layer"):
        st.markdown(
            """
            - The explanation combines extracted evidence, ranked conditions, and override state.
            - Non-urgent cases get a short rationale plus a safe next-step recommendation.
            - Urgent cases explicitly state that the override takes priority over the ranking.
            """
        )

    with st.sidebar.expander("5. Evaluation Layer"):
        st.markdown(
            f"""
            - Benchmarks are defined in `config/benchmark_cases.yaml`.
            - Evaluation summaries are written to `docs/evaluation_summary.md` and `.json`.
            - Current benchmark snapshot:
              - Parser F1: `{benchmark_summary['parser']['f1']:.3f}`
              - Top-1 accuracy: `{benchmark_summary['ranking']['top1_accuracy']:.3f}`
              - Top-2 recall: `{benchmark_summary['ranking']['top2_recall']:.3f}`
              - Safety recall: `{benchmark_summary['safety']['recall']:.3f}`
            """
        )

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

        if show_demo_notes:
            with st.expander("How this works: Extracted Evidence"):
                st.markdown(
                    """
                    The parser maps free text to a fixed backend schema using phrase matching and simple negation handling.
                    Unmentioned variables remain `unknown`, which keeps later inference steps auditable.
                    """
                )

        st.subheader("Safety Override")
        if bool(override["triggered"]):
            st.error(str(override["message"]))
            st.caption(f"Triggered rule: {override['rule_id']}")
        else:
            st.success("No urgent override triggered from the currently recognized evidence.")

        if show_demo_notes:
            with st.expander("How this works: Safety Override"):
                st.markdown(
                    """
                    This section is driven by hard-coded symbolic rules from `config/safety_rules.yaml`.
                    If a red-flag rule fires, that warning takes precedence over the probabilistic condition ranking.
                    """
                )

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

        if show_demo_notes:
            with st.expander("How this works: Condition Ranking"):
                st.markdown(
                    """
                    The ranking layer combines condition priors and evidence likelihoods from the YAML CPT files in `config/cpts/`.
                    It currently scores the four modeled conditions and normalizes them into posterior probabilities.
                    """
                )

        st.subheader("Explanation")
        st.write(str(response["explanation"]))

        if show_demo_notes:
            with st.expander("How this works: Explanation"):
                st.markdown(
                    """
                    The explanation layer uses the extracted evidence, ranked conditions, and override status to produce a short justification.
                    It also keeps the messaging aligned with Responsible AI constraints such as uncertainty disclosure and non-diagnosis framing.
                    """
                )

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
