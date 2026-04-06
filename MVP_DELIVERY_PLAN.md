# Elderly Symptom Reasoning Assistant MVP Delivery Plan

## 1. Purpose

This document captures the narrowed MVP plan for the CS3263 application project after reviewing:

- the original proposal in `/Users/adityaghosh/Desktop/CS3263/Project/CS3263 Group 7 Project Proposal.pdf`
- the module guidelines in `/Users/adityaghosh/Desktop/CS3263/Project/CS3263-Project-Guidelines 2526-2.pdf`
- the professor's feedback to tighten scope, define targeted tasks, explain the knowledge source, and state how success will be measured
- the follow-up scoped MVP notes and dataset references

This version of the plan assumes that the **MVP implementation is my primary responsibility**, while the rest of the team focuses mainly on the report and related project materials. The goal is to deliver a credible, demo-ready MVP by the **end of this week**, leaving the following week for presentation and report polishing before the final report deadline on **Sunday, 19 April 2026**.

## 2. Final MVP Scope

### In-scope

We will build an **explainable Bayesian reasoning assistant for vague elderly symptom descriptions**. The MVP will:

1. accept a short free-text symptom description
2. map it into a small structured evidence set
3. use a Bayesian network with exact inference to rank a few plausible conditions
4. trigger hard safety overrides for urgent red-flag scenarios
5. return probabilities, a short explanation, and a safe next-step recommendation

### Modeled conditions

- dehydration
- hypoglycemia
- mild viral infection
- medication side effect

### Modeled context variables

- skipped meal
- low water intake
- poor sleep
- chronic condition flag

### Modeled symptoms

- dizziness
- fatigue
- dry mouth
- headache
- mild fever
- nausea
- sweating
- confusion

### Red-flag override inputs

- chest pain
- severe confusion
- fainting
- recent fall

### Out-of-scope

The following are intentionally removed from the proposal for feasibility and clarity:

- medication scheduling
- PDDL planning
- full FOL reasoning
- broad disease coverage
- end-to-end diagnosis claims
- deployment with real patient data
- heavy LLM-first reasoning architecture

## 3. Project Positioning

The strongest framing for this project is:

> We develop an explainable Bayesian reasoning MVP that converts vague symptom descriptions into structured evidence, ranks a small set of plausible elderly health conditions under uncertainty, and safely escalates urgent red-flag scenarios.

This aligns well with the course guidelines because it emphasizes:

- problem formulation under uncertainty
- AI techniques covered in class
- technical depth through Bayesian networks and variable elimination
- responsible AI through transparency, disclaimers, and escalation
- a scoped application project that can be implemented and evaluated within the remaining time

## 4. Knowledge Source Strategy

The professor explicitly asked about the source of knowledge going into the system. The MVP should therefore use a **hybrid, human-auditable knowledge source** rather than claim learned medical expertise.

### Primary knowledge inputs

1. Public symptom-condition references
   - Use trusted public health references to justify symptom associations and safety rules.
   - Candidate sources already discussed: CDC, Mayo Clinic, WHO, HealthHub Singapore.
   - These sources support symptom plausibility and safe next-step language, not formal diagnosis.

2. Reduced public datasets
   - Kaggle disease-symptom dataset:
     - use for selecting a manageable symptom/condition subset
     - use for rough association checks and synthetic case design
     - do not use as a direct full-disease prediction target
   - CSympData expert-annotated symptom dataset:
     - use for vague patient phrasing
     - use for parser normalization examples
     - use for reduced-set symptom extraction evaluation
   - OpenReview paper:
     - use for related work, positioning, and evaluation framing
     - do not use as training data

3. Explicit expert-designed assumptions
   - Conditional probability tables will be literature-informed and manually authored.
   - Every major CPT assumption should be documented in a human-readable file.
   - The report should clearly state that the system is a teaching/demo prototype and not clinically validated.

### Knowledge-source principle

Every rule, probability, and recommendation in the MVP should be traceable to one of:

- a public reference
- a reduced dataset artifact
- an explicitly documented project assumption

## 5. Success Criteria

Success must be measurable, because this was a direct point in the professor's feedback.

### Metric 1: parser quality

- Task: map vague symptom text into the reduced evidence schema
- Evaluation set: manually labeled reduced examples from CSympData plus team-authored prompts
- Metric: precision, recall, F1 on the reduced symptom set
- MVP target: **F1 >= 0.75**

### Metric 2: condition ranking quality

- Task: rank plausible conditions from structured evidence
- Evaluation set: synthetic benchmark cases with expected target conditions
- Metrics:
  - Top-1 accuracy
  - Top-2 recall
- MVP targets:
  - **Top-1 accuracy >= 0.75**
  - **Top-2 recall >= 0.90**

### Metric 3: safety recall

- Task: escalate urgent red-flag cases
- Evaluation set: manually authored emergency cases
- Metric: recall on red-flag scenarios
- MVP target: **100% recall on emergency cases**

### Metric 4: explanation usefulness

- Task: help a user understand why the system suggested a condition or escalation
- Evaluation set: small teammate or classmate feedback sample
- Metric: average clarity rating on a 5-point scale
- MVP target: **>= 4.0 / 5**

## 6. MVP Architecture

### Module A: symptom parser

- input: free-text symptom description
- method: keyword and phrase normalization with a synonym map and basic negation handling
- output: structured evidence dictionary with `yes`, `no`, or `unknown` values

### Module B: Bayesian network core

- small, interpretable network
- context variables influence latent causes
- latent causes influence symptom variables
- exact inference via variable elimination
- output: posterior scores for the four modeled conditions

### Module C: safety override layer

- simple rules with explicit precedence over probabilistic outputs
- example overrides:
  - chest pain -> urgent escalation
  - severe confusion -> urgent escalation
  - fainting -> urgent escalation
  - dizziness + recent fall -> urgent escalation

### Module D: explanation layer

- report top conditions and their probabilities
- mention the strongest observed evidence
- include uncertainty disclosure
- include safe next-step guidance
- include a clear non-diagnosis disclaimer

### Module E: demo interface

- lightweight CLI or Streamlit app
- accept one free-text symptom input
- display:
  - extracted evidence
  - ranked condition probabilities
  - override warning if triggered
  - explanation and safe advice

### Module F: demo notes layer

- presentation-only UI notes that explain how each module works in the backend
- intended for grader/demo use, not for real elderly end users
- should explain:
  - how symptom parsing works
  - how safety overrides work
  - how Bayesian ranking works
  - how explanation generation works
  - how benchmark evaluation is measured

## 7. Implementation Tasks for This Week

This section lists the work that needs to be completed for a feature-complete MVP by the end of this week. The order below is recommended, but it does not need to be tied to specific days.

### 1. Lock the exact problem schema

- finalize the four modeled conditions
- finalize the symptom variables, context variables, and red-flag inputs
- define allowed values for each variable
- write down the canonical evidence schema that every module will use

Completion criteria:

- scope is frozen
- variable names and values are consistent
- downstream modules can rely on one stable schema

### 2. Prepare the reduced knowledge assets

- ingest the Kaggle disease-symptom dataset and reduce it to the chosen scope
- extract useful vague phrasing examples from CSympData
- create a symptom synonym and phrase mapping table
- start a knowledge-source register and a CPT assumption log

Completion criteria:

- reduced symptom-condition references are saved
- parser phrase mappings exist in a usable form
- assumptions and source provenance are documented

### 3. Build the symptom parser

- implement phrase-to-symptom normalization
- handle common negations such as "no fever" and "not dizzy"
- map free text into a structured evidence dictionary
- add a small parser test set for the reduced symptom space

Completion criteria:

- free-text input can be converted into the reduced evidence schema
- parser behavior is stable on representative vague inputs

### 4. Build the Bayesian network core

- encode the network structure
- store CPTs in a readable, editable format
- implement or connect exact inference via variable elimination
- test posterior outputs on hand-designed benchmark cases

Completion criteria:

- the network returns probabilities for all four conditions
- results look sensible on benchmark examples

### 5. Build the safety override layer

- implement deterministic urgent escalation rules
- enforce precedence of override rules over non-urgent probabilistic outputs
- test clear emergency and non-emergency cases

Completion criteria:

- red-flag cases always trigger escalation
- benign cases continue through the normal ranking flow

### 6. Build the explanation and advice layer

- generate ranked condition output
- surface the main evidence behind the output
- add safe next-step guidance
- add a clear disclaimer that the system is not providing diagnosis

Completion criteria:

- each output is understandable and appropriately cautious
- the wording supports explainability and responsible AI framing

### 7. Integrate the end-to-end pipeline

- connect parser, Bayesian inference, safety rules, and explanation generation
- ensure one input flow produces one consistent final result
- handle missing or unknown evidence gracefully

Completion criteria:

- the system works from free text to final response
- outputs are internally consistent across modules

### 8. Run evaluation and fix the biggest failure cases

- evaluate parser precision, recall, and F1
- evaluate Top-1 accuracy and Top-2 recall for condition ranking
- evaluate emergency escalation recall
- inspect failure cases and patch the highest-impact issues

Completion criteria:

- headline metrics are available
- main failure modes are documented
- the MVP is stable enough to demo

### 9. Prepare demo and report-ready artifacts

- build or polish a minimal Streamlit or CLI demo
- prepare one benign ambiguous case and one urgent escalation case
- capture screenshots, outputs, and metric summaries
- summarize knowledge sources, assumptions, limitations, and results for reuse in the report

Completion criteria:

- the MVP is demo-ready
- there are polished example cases ready for presentation
- report-writing inputs are available without extra implementation work

## 8. Suggested Repository Structure

The repo should grow into this layout during the week:

```text
elderly-care-mvp/
  app/
  config/
    cpts/
  data/
    raw/
    processed/
  docs/
  notebooks/
  src/
    parser/
    bn/
    rules/
    explain/
    eval/
  tests/
  .gitignore
  MVP_DELIVERY_PLAN.md
  README.md
  requirements.txt
```

## 9. Ownership Assumptions

This plan assumes the MVP is being built primarily by **Aditya** and should be executable without depending on parallel implementation from teammates.

Supporting assumptions:

- report-writing by teammates should not block MVP implementation
- any feedback or testing help from teammates is useful but optional
- architecture and tooling choices should favor speed, clarity, and solo maintainability
- documentation should be good enough that teammates can still explain the MVP in the final presentation

## 10. Risks and Mitigations

### Risk: CPTs are too arbitrary

Mitigation:

- keep the network small
- cite public references where possible
- store assumptions explicitly
- evaluate on synthetic cases instead of claiming medical validity

### Risk: parser quality is weak on vague phrasing

Mitigation:

- stay with a reduced symptom set
- use CSympData examples to seed synonyms
- prioritize high-frequency phrases first

### Risk: scope creeps back toward the original proposal

Mitigation:

- reject planning, scheduling, and richer diagnostic coverage for this MVP
- treat any extra feature as post-MVP only

### Risk: strong results are hard to show quickly

Mitigation:

- use a curated benchmark set
- design benchmark cases early
- prioritize reliability on a small problem over breadth

## 11. End-of-Week MVP Deliverables

By the end of this week, the MVP should include:

1. a working parser for the reduced symptom set
2. a working Bayesian inference module
3. a working safety override layer
4. a working explanation generator
5. a small end-to-end demo interface
6. evaluation scripts with headline metrics
7. documented knowledge sources and assumptions
8. two polished demo cases for presentation

## 12. Refinement Phase

The core MVP is now implemented. The remaining work is a refinement phase focused on improving coverage, grounding, and demo clarity without breaking the scoped project story.

### Refinement goal 1: ingest the external datasets

- download and store the Kaggle disease-symptom dataset in `data/raw/`
- download and store the CSympData dataset in `data/raw/`
- keep a short note on what each dataset is used for
- avoid treating the datasets as end-to-end training sources

Current repo-side progress:

- raw-data subfolders have been prepared for OpenReview, Figshare, and Kaggle sources
- a tracked ingestion note has been added in `docs/data_ingestion.md`
- a helper script has been added at `scripts/fetch_external_data.sh`
- source files have now been placed under `data/raw/openreview/`, `data/raw/figshare/`, and `data/raw/kaggle/`

### Refinement goal 2: expand parser phrasing from real examples

- use CSympData phrasing examples to broaden the symptom lexicon
- add more natural variants for existing symptoms before adding many new variables
- prioritize phrases that improve the current demo cases and benchmark failures
- keep the canonical output schema stable unless there is a strong reason to expand it

### Refinement goal 3: cautiously expand modeled coverage

The current MVP is intentionally small, but the extracted symptoms and modeled conditions can feel limited in a demo. Refinement should therefore focus on **controlled expansion**, not open-ended growth.

Recommended approach:

- first expand parser coverage for the existing four conditions
- then consider adding a small number of extra symptom variables if they materially improve realism
- only consider expanding the condition list if:
  - the added condition is still low-risk and explainable
  - it improves demo breadth
  - it does not break the scoped story of the project

### Refinement goal 4: tighten CPT assumptions with stronger cited sources

- replace loosely chosen starter values with more clearly justified ones
- document source-backed rationale in `docs/cpt_assumptions.md`
- ensure the report can explain where each major probability choice came from

Current repo-side progress:

- a dedicated grounding note has been added in `docs/cpt_grounding.md`
- `docs/cpt_assumptions.md` now distinguishes project priors from symptom-level anchors
- `docs/knowledge_sources.md` now includes explicit public-source links used to justify symptom relevance
- the viral-condition symptom likelihoods have been slightly recalibrated to better match the cited references without changing the reduced 4-condition scope

### Refinement goal 5: enlarge benchmark coverage and tune failure cases

- add more parser cases with natural language variation
- add more ambiguous ranking cases
- add more negative cases for safety overrides
- use benchmark failures to drive targeted parser and CPT fixes

Current repo-side progress:

- the tracked benchmark set has been expanded with additional parser edge cases, ranking overlap cases, and negative override cases
- evaluation coverage now includes sparse-input parsing, negated red-flag phrasing, multi-rule precedence, and closer dehydration-vs-medication / dehydration-vs-hypoglycemia comparisons
- the evaluation summary artifact now surfaces benchmark set sizes so the broader coverage is visible in the generated report output

### Refinement goal 6: add demo-oriented backend notes in the UI

- add a demo-only section in the Streamlit app explaining each module
- keep the notes concise and clearly labeled as presentation aids
- possible placement:
  - collapsible expander sections under each output block
  - or a dedicated "How this works" sidebar section

The UI notes should explain:

- parser: phrase matching, synonym handling, negation handling
- safety layer: rule-based overrides from `config/safety_rules.yaml`
- ranking layer: priors + evidence likelihoods from YAML-backed CPT files
- explanation layer: explanation built from extracted evidence, ranking, and override state
- evaluation layer: benchmark-driven metrics written to `docs/evaluation_summary.md`

## 13. Report and Presentation Implications

This MVP plan also supports the final report structure required by the course.

### Strong report narrative

- problem: reasoning over vague symptoms under uncertainty
- method: Bayesian network plus rule-based escalation
- responsible AI: uncertainty disclosure, safety override, no-diagnosis framing
- evaluation: parser quality, ranking quality, safety recall, explanation clarity
- limitations: synthetic evaluation and manually authored knowledge

### Strong presentation narrative

- show the narrowed scope clearly
- explain why scope reduction improved technical depth and feasibility
- demo one benign case and one urgent case
- explain success metrics before showing results

## 14. Immediate Next Actions

The highest-priority next implementation steps are:

1. broaden benchmark coverage with more ambiguous cases, negative override cases, and parser edge cases
2. finish tightening the evaluation workflow and document the intended way to run it locally
3. reassess whether a very small condition or symptom-schema expansion is actually justified after the broader benchmark pass

## 15. Non-Negotiable Guardrails

- do not present the system as a medical diagnostic tool
- do not claim clinical validation
- do not expand scope carelessly; any condition expansion must stay small and justified
- do not let the UI work delay parser, BN, or evaluation
- do not let presentation-oriented UI notes distort the actual backend logic
- do not ship without a visible disclaimer and urgent escalation path

## 16. Implementation Progress

Completed checkpoints:

- repository scaffold and local Git setup completed
- parser checkpoint completed:
  - YAML-backed parser config loader added
  - canonical `yes/no/unknown` evidence schema implemented
  - phrase-based symptom, context, and red-flag extraction implemented
  - simple negation handling implemented
  - parser tests added
  - Streamlit app updated to preview extracted evidence
- safety override checkpoint completed:
  - YAML-backed safety rule loader added
  - deterministic override matching implemented
  - urgent override output integrated into the app
  - safety rule tests added
- Bayesian ranking checkpoint completed:
  - YAML-backed priors and evidence likelihoods added
  - posterior ranking implementation added
  - condition ranking integrated into the app
  - Bayesian ranking tests added
- explanation checkpoint completed:
  - explanation generation added from evidence, ranking, and overrides
  - safe next-step recommendation generation added
  - visible disclaimer added to the app
  - explanation tests added
- evaluation checkpoint completed:
  - tracked benchmark cases added
  - parser, ranking, and safety metrics implemented
  - runnable evaluation artifact generation added
  - report-ready evaluation summary generation added
- demo-note UI checkpoint completed:
  - presentation-only backend explanation notes added to the Streamlit UI
  - sidebar "Show demo notes" control added
  - section-level "How this works" explainers added for demo use
- dataset-ingestion preparation checkpoint completed:
  - raw-data source folders created
  - tracked ingestion guidance added
  - helper fetch script added
- dataset-ingestion checkpoint completed:
  - OpenReview paper placed in `data/raw/openreview/OpenReview.pdf`
  - CSympData file placed in `data/raw/figshare/FigShare.csv`
  - Kaggle dataset file placed in `data/raw/kaggle/kaggle.csv`
  - ingestion notes updated to reflect the actual files present
- data-tracking policy checkpoint completed:
  - `.gitignore` updated to allow tracked small raw files and committed processed artifacts
  - large Kaggle raw file kept ignored by default
  - `data/processed/README.md` added to clarify what should be committed
- dataset-driven parser expansion checkpoint completed:
  - lexicon expanded using real phrasing from FigShare and Kaggle sources
  - schema kept stable while phrase coverage increased
  - processed phrase-expansion notes added to `data/processed/parser_phrase_expansion.md`
  - parser tests added for the new dataset-derived wording
- benchmark-driven parser expansion checkpoint completed:
  - additional high-frequency missed phrases identified from dataset review
  - parser coverage expanded for phrases such as `feeling sick`, `lost appetite`, and `chills`
  - benchmark cases updated to reflect the new parser coverage
  - parser and evaluation suite rerun successfully after the update
- CPT-grounding checkpoint completed:
  - `docs/cpt_grounding.md` added to explain how public references map to demo probabilities
  - `docs/cpt_assumptions.md` strengthened with clearer priors, symptom anchors, and source-backed rationale
  - `docs/knowledge_sources.md` updated with explicit source URLs for the currently modeled conditions
  - mild viral infection likelihoods slightly recalibrated to better reflect the cited symptom references
- broader benchmark coverage checkpoint completed:
  - parser benchmarks expanded with additional natural-language variants, sparse-input coverage, and negation cases
  - ranking benchmarks expanded with additional overlap cases and explicit negative-evidence cases
  - safety benchmarks expanded with more non-trigger cases and a multi-rule precedence case
  - generated evaluation summary now reports benchmark set sizes alongside headline metrics

Next logical implementation slice:

- refinement phase:
  - evaluation-command reliability and usage cleanup
  - controlled decision on whether any small coverage expansion is still worth it

This plan gives a single primary implementer a realistic path to a high-scoring, course-aligned MVP within one week while staying faithful to the professor's feedback and the grading rubric.
