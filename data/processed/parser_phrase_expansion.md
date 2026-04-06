# Parser Phrase Expansion Notes

This file records the first dataset-driven parser expansion pass after ingesting the external sources.

## Added phrases mapped to the current schema

These phrases were added to `config/symptom_lexicon.yaml` without changing the core evidence schema.

### Dizziness

- `dizziness`
- `lightheadedness`
- `feeling lightheaded`
- `feeling lightheaded when standing`
- `sensation of spinning`
- `feeling dizzy`
- `feeling faint`
- `feeling faint upon standing`

### Fatigue

- `fatigue`
- `feeling tired`
- `extreme tiredness`
- `tiredness`
- `feeling unusually tired`
- `weakness`
- `muscle weakness`
- `feeling weak`
- `a feeling of weakness`

### Dry mouth / thirst proxy

- `mouth dryness`
- `feeling thirsty`
- `increased thirst`
- `thirst`

### Headache

- `headaches`
- `morning headache`
- `frontal headache`

### Mild fever

- `feeling warm`
- `feeling hot`

### Sweating

- `profuse sweating`
- `night sweats`
- `cold sweat`
- `cool clammy skin`
- `feeling sweaty`
- `sweat`

### Confusion

- `confusion`
- `confused thinking`
- `disorientation`

### Red flags

- `sharp chest pain`
- `stabbing chest pain`
- `burning chest pain`
- `loss of consciousness`
- `falls`

## Main source signals

The following phrases were directly observed in the ingested data sources and motivated this update:

- from `data/raw/figshare/FigShare.csv`:
  - `feeling tired`
  - `sensation of spinning`
  - `feeling lightheaded`
  - `extreme tiredness`
  - `increased thirst`
  - `profuse sweating`
  - `loss of consciousness`
  - `burning chest pain`
  - `confused thinking`

- from `data/raw/kaggle/kaggle.csv`:
  - `dizziness`
  - `fainting`
  - `headache`
  - `nausea`
  - `mouth dryness`
  - `thirst`
  - `weakness`
  - `fatigue`
  - `fever`
  - `chest tightness`

## Deferred candidates for possible schema expansion

These appeared in the data but were not added to the current schema yet:

- `shortness breath`
- `blurred vision`
- `loss of appetite`
- `chills`
- `fast heart rate`

These may become future symptom variables if benchmark-driven refinement shows that they would materially improve the MVP.

## Benchmark-driven refinement notes

After the first dataset-driven pass, the following additional phrases were promoted because they appeared frequently and exposed visible parser gaps during refinement:

- `feeling sick`
- `feeling sick overall`
- `feeling ill`
- `lost appetite`
- `decreased appetite`
- `chills`

These are currently mapped into the existing fatigue and mild-fever style variables rather than triggering a schema expansion.
