# Elderly Symptom Reasoning Assistant

An explainable Bayesian MVP for preliminary reasoning over vague elderly health symptoms.

## Overview

This repository contains the MVP for a CS3263 application project on reasoning under uncertainty. The system accepts a short free-text symptom description, maps it into a reduced evidence schema, ranks a small set of plausible conditions, applies urgent safety overrides, and returns an explanation plus safe next-step guidance.

The project is intentionally narrow. It is designed as a course-aligned demonstration of Bayesian reasoning, safety-oriented rule overrides, explainability, and benchmark-driven evaluation.

This system is **not** a medical diagnostic tool and has not been clinically validated.

## MVP Scope

### Modeled conditions

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

## Core Capabilities

- free-text symptom parsing with phrase matching and basic negation handling
- Bayesian ranking over a reduced four-condition space
- deterministic safety overrides for urgent red-flag scenarios
- explanation and recommendation generation with a visible non-diagnosis disclaimer
- Streamlit demo interface with presentation-oriented backend notes
- benchmark evaluation for parser quality, ranking quality, and safety recall

## Architecture

The current MVP is organized into five main layers:

1. `src/parser/`
   Maps vague natural-language symptom descriptions into a fixed `yes` / `no` / `unknown` evidence schema.
2. `src/bn/`
   Scores the modeled conditions using YAML-backed priors and evidence likelihoods.
3. `src/rules/`
   Applies symbolic urgent-escalation rules that take precedence over probabilistic ranking.
4. `src/explain/`
   Produces user-facing explanation text, recommendation text, and disclaimer output.
5. `src/eval/`
   Runs benchmark cases and writes report-ready evaluation summaries.

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

## Getting Started

Development was done with Python 3.11. Running everything from the repository root is recommended.

### 1. Create an environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

If Conda is preferred instead of `venv`, make sure `python3`, `pip`, and Streamlit all come from the same active environment.

## Running the Demo App

```bash
python3 -m streamlit run app/streamlit_app.py
```

The app provides:

- a dark-mode landing state with example prompts
- a single-input / single-output demo flow
- extracted evidence, safety override, condition ranking, explanation, and recommendation sections
- optional sidebar demo notes for presentation use

## Running the Evaluation Pipeline

```bash
python3 -m src.eval
```

This command runs the tracked benchmark set and writes:

- `docs/evaluation_summary.md`
- `docs/evaluation_summary.json`

The benchmark cases are defined in:

- `config/benchmark_cases.yaml`

## Running the Test Suite

```bash
pytest -q
```

## Data and Knowledge Sources

The repository includes documentation for both raw-data handling and manual knowledge grounding.

Key references:

- `docs/data_ingestion.md`
- `docs/knowledge_sources.md`
- `docs/cpt_assumptions.md`
- `docs/cpt_grounding.md`
- `docs/evaluation_summary.md`

The full raw datasets are not required to run the app, the tests, or the benchmark evaluation pipeline.

## Evaluation Purpose

The evaluation layer is intended for project analysis and reporting rather than end-user interaction. It measures:

- parser precision, recall, and F1
- ranking Top-1 accuracy
- ranking Top-2 recall
- safety recall and accuracy

The current benchmark suite is synthetic / hand-authored for the reduced MVP scope.

## Limitations

- the condition space is intentionally limited to four modeled conditions
- the CPTs are hand-authored and source-grounded, not learned from clinical outcome data
- the evaluation is benchmark-based and not a substitute for medical validation
- the recommendations are conservative next-step prompts, not treatment advice

## Troubleshooting

### `ModuleNotFoundError: No module named 'yaml'`

Install the dependencies in the same environment used to run the app or evaluation:

```bash
python3 -m pip install -r requirements.txt
```

### Streamlit runs but `python3 -m src.eval` fails

This usually indicates an environment mismatch. Activate the same environment and rerun:

```bash
source .venv/bin/activate
python3 -m src.eval
```

### Resetting the demo interface

Use the app's `Clear` button to return to the landing state and remove the current analysis output.
