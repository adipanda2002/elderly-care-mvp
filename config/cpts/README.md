# CPT Files

This directory stores the human-readable probability inputs for the Bayesian network.

Suggested file split:

- `condition_priors.yaml`: priors for the four modeled conditions
- `symptom_likelihoods.yaml`: symptom probabilities conditioned on each condition
- optional future files for context-condition links if the network grows

All values should be literature-informed or explicitly documented as project assumptions.
