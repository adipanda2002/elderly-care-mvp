# External Data Ingestion

This document records the external sources intended for ingestion into `data/raw/` and how they should be used in the MVP.

## Status

The external source files have now been placed into the repo and organized under `data/raw/`.

Prepared raw-data folders:

- `/Users/adityaghosh/Desktop/CS3263/Project/elderly-care-mvp/data/raw/openreview/`
- `/Users/adityaghosh/Desktop/CS3263/Project/elderly-care-mvp/data/raw/figshare/`
- `/Users/adityaghosh/Desktop/CS3263/Project/elderly-care-mvp/data/raw/kaggle/`

## Source 1: OpenReview paper

- URL: <https://openreview.net/forum?id=heBKnuV42O>
- Title: `DDXPlus: A New Dataset For Automatic Medical Diagnosis`
- Intended repo location:
  - `data/raw/openreview/OpenReview.pdf`

Use in project:

- related work
- design motivation
- framing for explainability and diagnosis-style symptom reasoning

## Source 2: CSympData dataset

- URL: <https://figshare.com/articles/dataset/CSympData_Expert_Annotated_Patient_Symptoms_Data/28547042?file=57688621>
- Intended repo location:
  - `data/raw/figshare/FigShare.csv`

Use in project:

- real phrasing examples for symptom parser expansion
- benchmark-driven lexicon enrichment
- reduced-set parser evaluation examples

## Source 3: Kaggle diseases-and-symptoms dataset

- URL: <https://www.kaggle.com/datasets/dhivyeshrk/diseases-and-symptoms-dataset>
- Intended repo location:
  - `data/raw/kaggle/kaggle.csv`

Use in project:

- selecting or validating a small symptom-condition subset
- cross-checking symptom-condition associations
- constructing synthetic benchmark cases

## Current file inventory

- `data/raw/openreview/OpenReview.pdf`
- `data/raw/figshare/FigShare.csv`
- `data/raw/kaggle/kaggle.csv`

## Notes for report transparency

- The external sources are used for grounding, parser coverage, and benchmarking.
- The project should not claim clinical validation from these files.
- The Kaggle dataset should not be presented as direct real-patient evidence.

## Git tracking policy

- `data/raw/openreview/OpenReview.pdf` is allowed to be tracked
- `data/raw/figshare/FigShare.csv` is allowed to be tracked
- `data/raw/kaggle/kaggle.csv` remains ignored by default because it is large
- `data/processed/` is intended for small committed derived artifacts that help teammates reproduce the MVP
