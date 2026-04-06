# CPT Files

This directory stores the human-readable probability inputs for the Bayesian network.

Suggested file split:

- `condition_priors.yaml`: priors for the four modeled conditions
- `symptom_likelihoods.yaml`: probabilities of `yes` for each modeled evidence variable conditioned on each condition

Current simplified format:

- `P(condition)` comes from `condition_priors.yaml`
- `P(variable=yes | condition)` comes from `symptom_likelihoods.yaml`
- `P(variable=no | condition)` is treated as `1 - P(variable=yes | condition)`
- `unknown` evidence is ignored during scoring

All values should be literature-informed or explicitly documented as project assumptions.
