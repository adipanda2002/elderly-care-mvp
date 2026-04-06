# CPT Assumptions Log

Use this file to document the rationale for each major Bayesian probability choice.

| Item | Planned value | Rationale | Source or assumption |
| --- | --- | --- | --- |
| `P(dehydration)` | `0.34` | Common low-risk explanation for vague dizziness, dry mouth, and fatigue in a small elderly-wellbeing MVP | Project assumption informed by public dehydration symptom references |
| `P(hypoglycemia)` | `0.16` | Narrower target condition, but important because skipped meals and sweating should still rank strongly | Project assumption informed by public hypoglycemia symptom references |
| `P(mild_viral_infection)` | `0.30` | Plausible common explanation for fatigue plus mild fever in a limited symptom model | Project assumption informed by public viral symptom references |
| `P(medication_side_effect)` | `0.20` | Included because elderly users often have ongoing medication exposure and overlapping mild symptoms | Project assumption informed by proposal background and public side-effect guidance |
| `P(dry_mouth=yes \| dehydration)` | `0.85` | Dry mouth is one of the strongest dehydration cues in the reduced feature set | Public symptom guidance + project simplification |
| `P(sweating=yes \| hypoglycemia)` | `0.80` | Sweating is intended to be a strong differentiator for low blood sugar in the MVP | Public symptom guidance + project simplification |
| `P(mild_fever=yes \| mild_viral_infection)` | `0.85` | Mild fever should strongly favor viral infection relative to the other three conditions | Public symptom guidance + project simplification |
| `P(nausea=yes \| medication_side_effect)` | `0.65` | Nausea is used as a meaningful but not decisive indicator for medication side effect | Public side-effect references + project simplification |

These values are starter assumptions for the MVP and should be refined as dataset analysis and benchmark tuning progress.
