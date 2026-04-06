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
python3 -m pip install -r requirements.txt
```

If you are using Conda instead of `venv`, make sure `python3`, `pip`, and `streamlit` all come from the same active environment before running the app or evaluation commands.

## Run the App

```bash
streamlit run app/streamlit_app.py
```

## Run Evaluation

```bash
python3 -m src.eval
```

This command:

- runs the parser, ranking, and safety benchmarks defined in `config/benchmark_cases.yaml`
- writes report-ready summaries to `docs/evaluation_summary.md` and `docs/evaluation_summary.json`

If you see `ModuleNotFoundError: No module named 'yaml'`, install the project dependencies in the same environment:

```bash
python3 -m pip install -r requirements.txt
```

## External Data

The raw-data folders are prepared under `data/raw/`. Source notes live in:

- `docs/data_ingestion.md`

If you later want to fetch the external files from the command line, a helper script is available:

```bash
bash scripts/fetch_external_data.sh
```

Note:

- the OpenReview paper and Figshare dataset can be fetched directly when network access is allowed
- the Kaggle dataset usually requires authenticated/manual download

## Current Status

This is the initial scaffold commit. The next build steps are:

1. ingest the reduced datasets into `data/raw/`
2. expand the parser lexicon with dataset-driven phrasing
3. refine CPT assumptions with stronger source grounding
4. iterate on benchmark failures and demo polish
