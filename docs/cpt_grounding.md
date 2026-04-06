# CPT Grounding Notes

This document explains how the current Bayesian probabilities are grounded.

## Grounding approach

The current MVP does **not** claim to learn probabilities from clinical outcome data. Instead, the CPTs are grounded in:

1. official public-health or government-reviewed symptom references
2. reduced public datasets used only for vocabulary and scenario design
3. explicit project assumptions chosen to keep the MVP explainable and safe

## Qualitative-to-numeric mapping

The current numbers are not direct prevalence estimates. They are a small-model translation from qualitative evidence strength into stable demo probabilities.

- `0.75 - 0.85`
  Used when a symptom is presented as a strong or common signal for that modeled condition.
- `0.45 - 0.65`
  Used when a symptom is plausible and supportive, but not a strong differentiator.
- `0.05 - 0.30`
  Used when a symptom is weak, less emphasized, or mainly included to keep overlap realistic.

## Source-backed anchors

### Dehydration

Primary source:

- MedlinePlus dehydration page:
  - <https://medlineplus.gov/ency/article/000982.htm>

Relevant symptom anchors:

- thirst
- dry or sticky mouth
- headache
- dizziness or lightheadedness
- confusion in more severe cases

Model implication:

- `dry_mouth`, `low_water_intake`, and `dizziness` stay among the strongest dehydration-linked signals in the reduced model.

### Hypoglycemia

Primary source:

- CDC low blood sugar page:
  - <https://www.cdc.gov/diabetes/about/low-blood-sugar-hypoglycemia.html>

Relevant symptom anchors:

- sweating
- dizziness
- confusion
- weakness
- hunger
- not skipping meals helps avoid low blood sugar

Model implication:

- `skipped_meal` and `sweating` remain strong hypoglycemia-linked signals.
- `dizziness`, `fatigue`, and `confusion` remain moderate supportive signals.

### Mild viral infection

Primary sources:

- MedlinePlus common cold page:
  - <https://medlineplus.gov/commoncold.html>
- MedlinePlus mononucleosis page:
  - <https://medlineplus.gov/ency/article/000591.htm>

Relevant symptom anchors:

- common cold commonly includes headache and often has low fever or no fever in adults and older children
- mononucleosis includes fever, fatigue, headache, and loss of appetite

Model implication:

- `mild_fever`, `fatigue`, and `headache` remain the main viral-pattern signals
- the viral fever likelihood was kept high but reduced from the earlier placeholder value so the model does not overstate fever as universal across mild viral illnesses

### Medication side effect

Primary sources:

- NIA cognitive health and older adults:
  - <https://www.nia.nih.gov/health/brain-health/cognitive-health-and-older-adults>
- MedlinePlus bumetanide drug information:
  - <https://medlineplus.gov/druginfo/meds/a684051.html>
- MedlinePlus levodopa and carbidopa drug information:
  - <https://medlineplus.gov/druginfo/meds/a601068.html>

Relevant symptom anchors:

- medicines and combinations of medicines can cause confusion in older adults
- example drug references include dry mouth, thirst, nausea, vomiting, weakness, dizziness, and confusion-related concerns

Model implication:

- `chronic_condition_flag` remains a strong medication-side-effect context variable
- `nausea` and `dry_mouth` remain the most emphasized medication-side-effect symptoms in the reduced model

## Priors

The four condition priors in `config/cpts/condition_priors.yaml` should be read as **project priors for a reduced teaching/demo problem**, not as population prevalence estimates.

They are intended to:

- keep the four modeled conditions competitive in the demo
- slightly favor common low-risk explanations
- avoid underweighting medication-related explanations in an elderly-care context

## Current limitations

- these probabilities are hand-authored rather than statistically estimated
- the sources justify symptom relevance better than exact percentages
- future refinement should use dataset analysis and benchmark failures to tune the numbers further
