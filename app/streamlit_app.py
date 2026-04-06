"""Minimal Streamlit entrypoint for the MVP demo."""

from pathlib import Path
import sys

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.bn import rank_conditions
from src.eval import load_benchmark_summary
from src.explain import build_response
from src.parser import parse_free_text
from src.rules import evaluate_overrides


EXAMPLE_PROMPTS = [
    {
        "title": "Hydration Pattern",
        "prompt": "I did not drink much water today. My mouth feels very dry and I am a little dizzy.",
    },
    {
        "title": "Low Sugar Pattern",
        "prompt": "I skipped breakfast, feel sweaty and dizzy, and I am starting to feel weak.",
    },
    {
        "title": "Mild Viral Pattern",
        "prompt": "I feel tired, warm, and have a mild headache since this morning.",
    },
    {
        "title": "Urgent Override",
        "prompt": "I fainted and also have chest pain.",
    },
]


st.set_page_config(page_title="Elderly Symptom Reasoning Assistant", page_icon=":stethoscope:")


def _inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --app-bg: #0e1117;
            --surface: #171b24;
            --surface-hover: #1d2330;
            --border: #2c3444;
            --text: #f3f4f6;
            --muted: #9ca3af;
            --accent: #10a37f;
        }

        [data-testid="stAppViewContainer"] {
            background: var(--app-bg);
        }

        .block-container {
            max-width: 900px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .landing-shell {
            text-align: center;
            padding: 2.5rem 0 1.25rem 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .landing-eyebrow {
            color: var(--muted);
            font-size: 0.9rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            margin-bottom: 0.75rem;
        }

        .landing-title {
            color: var(--text);
            font-size: 3rem;
            font-weight: 700;
            line-height: 1.1;
            margin: 0;
        }

        .landing-subtitle {
            color: var(--muted);
            font-size: 1rem;
            margin: 1rem auto 0 auto;
            max-width: 560px;
            line-height: 1.6;
            text-wrap: balance;
        }

        .example-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1rem 1rem 0.5rem 1rem;
            min-height: 138px;
            box-shadow: 0 14px 30px rgba(0, 0, 0, 0.22);
            margin-bottom: 0.5rem;
        }

        .example-title {
            color: var(--text);
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 0.45rem;
        }

        .example-body {
            color: var(--muted);
            font-size: 0.95rem;
            line-height: 1.5;
        }

        .compact-subtitle {
            color: var(--muted);
            margin-bottom: 1rem;
        }

        .stButton > button {
            background: var(--surface);
            color: var(--text);
            border: 1px solid var(--border);
            border-radius: 12px;
        }

        .stButton > button:hover {
            background: var(--surface-hover);
            border-color: #3a4458;
            color: var(--text);
        }

        .stButton > button[kind="primary"] {
            background: var(--accent);
            border-color: var(--accent);
            color: #ffffff;
        }

        .stButton > button[kind="primary"]:hover {
            background: #0d8b6c;
            border-color: #0d8b6c;
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _ensure_state() -> None:
    st.session_state.setdefault("user_input", "")
    st.session_state.setdefault("analysis_result", None)
    st.session_state.setdefault("pending_scroll_to_results", False)


def _build_analysis_result(user_text: str) -> dict[str, object]:
    evidence = parse_free_text(user_text)
    extracted = {key: value for key, value in evidence.items() if value != "unknown"}
    override = evaluate_overrides(evidence)
    condition_scores = rank_conditions(evidence)
    response = build_response(evidence, condition_scores, override)

    return {
        "evidence": evidence,
        "extracted": extracted,
        "override": override,
        "condition_scores": condition_scores,
        "response": response,
    }


def _clear_app_state() -> None:
    st.session_state["user_input"] = ""
    st.session_state["analysis_result"] = None
    st.session_state["pending_scroll_to_results"] = False


def _use_example_prompt(prompt: str) -> None:
    st.session_state["user_input"] = prompt
    st.session_state["analysis_result"] = None
    st.session_state["pending_scroll_to_results"] = False
    st.rerun()


def _render_landing_intro() -> None:
    st.markdown(
        """
        <div class="landing-shell">
            <div class="landing-eyebrow">CS3263 Bayesian MVP</div>
            <h1 class="landing-title">Describe the symptoms</h1>
            <p class="landing-subtitle">
                A focused demo for vague symptom parsing, Bayesian ranking, safety overrides,
                and explainable next-step guidance.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for idx, example in enumerate(EXAMPLE_PROMPTS):
        with cols[idx % 2]:
            st.markdown(
                f"""
                <div class="example-card">
                    <div class="example-title">{example['title']}</div>
                    <div class="example-body">{example['prompt']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Use Example", key=f"example_{idx}", use_container_width=True):
                _use_example_prompt(example["prompt"])

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

_inject_styles()
_ensure_state()

if st.session_state["analysis_result"] is None:
    _render_landing_intro()
else:
    st.title("Elderly Symptom Reasoning Assistant")
    st.markdown(
        '<div class="compact-subtitle">Bayesian symptom reasoning demo with safety overrides and explainable outputs.</div>',
        unsafe_allow_html=True,
    )

st.text_area(
    "Describe the symptoms",
    key="user_input",
    placeholder="Example: I feel tired, slightly dizzy, and have a dry mouth.",
)

st.markdown('<div id="analysis-controls-anchor"></div>', unsafe_allow_html=True)

action_cols = st.columns([1, 1, 6])
analyze_clicked = action_cols[0].button("Analyze", type="primary", use_container_width=True)
action_cols[1].button(
    "Clear",
    use_container_width=True,
    disabled=not st.session_state["user_input"] and st.session_state["analysis_result"] is None,
    on_click=_clear_app_state,
)

if analyze_clicked:
    if not st.session_state["user_input"].strip():
        st.warning("Please enter a symptom description.")
    else:
        st.session_state["analysis_result"] = _build_analysis_result(st.session_state["user_input"].strip())
        st.session_state["pending_scroll_to_results"] = True

analysis_result = st.session_state["analysis_result"]

if analysis_result:
    extracted = dict(analysis_result["extracted"])
    override = dict(analysis_result["override"])
    response = dict(analysis_result["response"])

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

    if st.session_state["pending_scroll_to_results"]:
        components.html(
            """
            <script>
            const anchor = window.parent.document.getElementById("analysis-controls-anchor");
            if (anchor) {
                anchor.scrollIntoView({ behavior: "smooth", block: "center" });
            }
            </script>
            """,
            height=0,
        )
        st.session_state["pending_scroll_to_results"] = False
