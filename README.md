# Elderly Symptom Reasoning Assistant

An explainable Bayesian MVP for preliminary reasoning over vague elderly health symptoms.

## Current Status

This repo is now in a **demo-ready MVP state** for the CS3263 project.

The current app:

- accepts one free-text symptom description
- maps it into a reduced structured evidence schema
- ranks 4 modeled conditions with a Bayesian reasoning layer
- applies urgent safety overrides for red-flag cases
- returns explanation text, recommendation text, and a visible non-diagnosis disclaimer
- includes demo notes in the sidebar for presentation use

This system is **not** a medical diagnostic tool. It is a teaching/demo prototype for CS3263.

## Modeled Scope

### Conditions

- dehydration
- hypoglycemia
- mild viral infection
- medication side effect

### Context variables

- skipped meal
- low water intake
- poor sleep
- chronic condition flag

### Symptoms

- dizziness
- fatigue
- dry mouth
- headache
- mild fever
- nausea
- sweating
- confusion

### Red-flag overrides

- chest pain
- severe confusion
- fainting
- recent fall

## Repository Layout

```text
app/                 Streamlit demo app
config/              Variables, lexicon, rules, CPTs, and benchmark cases
data/                Raw and processed datasets / notes
docs/                Knowledge sources, assumptions, evaluation summaries
notebooks/           Optional exploration notebooks
src/                 Parser, BN, rules, explanation, and evaluation code
tests/               Test suite
```

## Teammate Setup

Run everything from the repository root.

### 1. Create and activate an environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If you prefer Conda, that is fine too, but make sure `python3`, `pip`, and Streamlit all come from the same active environment.

### 2. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 3. Run the demo app

Use the module form so the app definitely runs in the same Python environment that has the dependencies installed:

```bash
python3 -m streamlit run app/streamlit_app.py
```

Then open the local Streamlit URL in your browser.

### 4. Run the evaluation pipeline

```bash
python3 -m src.eval
```

This writes report-ready summaries to:

- `docs/evaluation_summary.md`
- `docs/evaluation_summary.json`

### 5. Run the tests

```bash
pytest -q
```

## What Teammates Need To Know

### For demo use

You do **not** need the large raw datasets to run the app, run tests, or run the evaluation pipeline.

The committed config files and benchmark files are enough for:

- the Streamlit demo
- the parser / BN / rules pipeline
- the benchmark evaluation

### For dataset analysis / further refinement

Raw-data notes are documented in:

- `docs/data_ingestion.md`

The project may contain:

- smaller tracked raw files for reference
- processed notes and mappings
- a large Kaggle raw file that is intentionally not required for normal app usage

## Demo Flow

Recommended teammate demo flow:

1. launch the Streamlit app
2. use one of the example cards or type a symptom description
3. click `Analyze`
4. review the extracted evidence
5. review the safety override
6. review the condition ranking, explanation, and recommendation
7. use the sidebar demo notes if you need to explain how the backend works
8. use `Clear` to reset back to the landing state

## Evaluation Purpose

The evaluation pipeline exists mainly for the report and presentation, not for end users.

It measures:

- parser precision / recall / F1
- ranking Top-1 accuracy
- ranking Top-2 recall
- safety recall / accuracy

The benchmark cases live in:

- `config/benchmark_cases.yaml`

## Key Docs

- `MVP_DELIVERY_PLAN.md`: current implementation plan and progress log
- `docs/knowledge_sources.md`: public-source grounding
- `docs/cpt_assumptions.md`: CPT assumptions
- `docs/cpt_grounding.md`: rationale for probability choices
- `docs/evaluation_summary.md`: benchmark summary

## Troubleshooting

### `ModuleNotFoundError: No module named 'yaml'`

Install dependencies in the same environment you are using to run the commands:

```bash
python3 -m pip install -r requirements.txt
```

### Streamlit runs but `python3 -m src.eval` fails

This usually means the app and `python3` are coming from different environments. Activate the same environment and rerun:

```bash
source .venv/bin/activate
python3 -m src.eval
```

### Resetting the demo

Use the app's `Clear` button to return to the landing state and remove the current results.
