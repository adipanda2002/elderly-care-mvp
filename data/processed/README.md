# Processed Data Policy

This folder is for **small, curated, reproducible artifacts** derived from the raw sources.

Examples that should be committed:

- reduced symptom phrase tables
- cleaned mapping files used by the parser
- benchmark subsets
- compact JSON, YAML, or CSV files that the MVP depends on

Examples that should usually not be committed here:

- very large derived exports
- temporary notebooks outputs
- one-off exploratory dumps that can be recreated easily

Current data policy:

- `data/raw/`
  - OpenReview PDF and FigShare CSV are allowed to be tracked
  - the large Kaggle raw file remains ignored by default
- `data/processed/`
  - small committed artifacts are encouraged when they improve reproducibility for the team
