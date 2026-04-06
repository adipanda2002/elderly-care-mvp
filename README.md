# Elderly Symptom Reasoning Assistant

An explainable Bayesian MVP for preliminary reasoning over vague elderly health symptoms.

## Scope

This project focuses on a small, safe, course-aligned MVP that:

- accepts a free-text symptom description
- maps it into a reduced evidence schema
- ranks four modeled conditions with Bayesian inference
- applies hard safety overrides for urgent red flags
- returns probabilities, explanation text, and safe next-step guidance

This system is **not** a medical diagnostic tool and is intended only as a teaching/demo prototype for CS3263.

## Initial Repository Layout

```text
app/                 Demo app entrypoint
config/              Human-readable variables, rules, lexicon, and CPT files
data/                Raw and processed datasets
docs/                Knowledge sources, assumptions, and benchmark notes
notebooks/           Optional exploration notebooks
src/                 Core parser, BN, rules, explanation, and evaluation code
tests/               Smoke tests and future unit tests
```

## Planned Core Modules

- `src/parser/`: vague symptom text normalization
- `src/bn/`: Bayesian network structure and inference
- `src/rules/`: urgent escalation overrides
- `src/explain/`: explanation and advice generation
- `src/eval/`: parser, ranking, and safety evaluation

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Current Status

This is the initial scaffold commit. The next build steps are:

1. ingest the reduced datasets into `data/raw/`
2. finalize the evidence schema and parser lexicon
3. fill in CPT assumptions and Bayesian inference
4. wire the end-to-end Streamlit demo
