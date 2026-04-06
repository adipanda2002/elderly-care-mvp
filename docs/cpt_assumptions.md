# CPT Assumptions Log

Use this file to document the rationale for each major Bayesian probability choice.

For the grounding method and source links, see:

- `/Users/adityaghosh/Desktop/CS3263/Project/elderly-care-mvp/docs/cpt_grounding.md`

## High-level assumptions

| Item | Current value | Rationale | Source or assumption |
| --- | --- | --- | --- |
| `P(dehydration)` | `0.34` | Common low-risk explanation for vague dizziness, dry mouth, and fatigue in a small elderly-wellbeing MVP | Project assumption informed by public dehydration symptom references |
| `P(hypoglycemia)` | `0.16` | Narrower target condition, but important because skipped meals and sweating should still rank strongly | Project assumption informed by public hypoglycemia symptom references |
| `P(mild_viral_infection)` | `0.30` | Plausible common explanation for fatigue plus mild fever in a limited symptom model | Project assumption informed by public viral symptom references |
| `P(medication_side_effect)` | `0.20` | Included because elderly users often have ongoing medication exposure and overlapping mild symptoms | Project assumption informed by proposal background and public side-effect guidance |

## Symptom-level anchors

| Item | Current value | Rationale | Source or assumption |
| --- | --- | --- | --- |
| `P(dry_mouth=yes \| dehydration)` | `0.85` | Dry or sticky mouth and thirst are strongly emphasized on dehydration references | MedlinePlus dehydration + project simplification |
| `P(dizziness=yes \| dehydration)` | `0.65` | Dizziness/lightheadedness is a strong supportive dehydration symptom but not fully specific | MedlinePlus dehydration + project simplification |
| `P(sweating=yes \| hypoglycemia)` | `0.80` | Sweating is one of the clearest low-blood-sugar symptoms on the CDC page | CDC hypoglycemia + project simplification |
| `P(dizziness=yes \| hypoglycemia)` | `0.60` | Dizziness is explicitly listed as a common low-blood-sugar symptom | CDC hypoglycemia + project simplification |
| `P(confusion=yes \| hypoglycemia)` | `0.30` | Confusion is supported, especially as symptoms worsen, but is not the main differentiator in the reduced model | CDC hypoglycemia + project simplification |
| `P(mild_fever=yes \| mild_viral_infection)` | `0.75` | Kept high but not maximal because some mild viral illnesses have low fever or no fever in adults | MedlinePlus common cold + mononucleosis + project simplification |
| `P(fatigue=yes \| mild_viral_infection)` | `0.70` | Fatigue/general ill feeling is strongly compatible with mild viral illness | MedlinePlus mononucleosis + project simplification |
| `P(headache=yes \| mild_viral_infection)` | `0.60` | Headache is common across viral upper-respiratory or mono-like illness patterns | MedlinePlus common cold + mononucleosis + project simplification |
| `P(nausea=yes \| medication_side_effect)` | `0.65` | Nausea is frequently listed on drug-information pages and is a meaningful but not exclusive medication-side-effect cue | MedlinePlus drug information + project simplification |
| `P(dry_mouth=yes \| medication_side_effect)` | `0.55` | Dry mouth is a recurring medication-side-effect signal, especially in older-adult medication contexts | MedlinePlus drug information + NIA older-adult medication caution |
| `P(confusion=yes \| medication_side_effect)` | `0.20` | Kept lower than nausea/dry mouth, but supported by older-adult medication guidance | NIA cognitive health and older adults + project simplification |

These values remain hand-authored starter assumptions and should still be refined as dataset analysis and benchmark tuning progress.
