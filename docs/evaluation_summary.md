# Evaluation Summary

## Headline Metrics

| Metric | Value | Target |
| --- | ---: | ---: |
| Parser F1 | 0.952 | 0.75 |
| Parser Precision | 1.000 | - |
| Parser Recall | 0.909 | - |
| Ranking Top-1 Accuracy | 0.833 | 0.75 |
| Ranking Top-2 Recall | 1.000 | 0.90 |
| Safety Recall | 1.000 | 1.00 |
| Safety Accuracy | 0.933 | - |

## Benchmark Coverage

| Benchmark Group | Cases |
| --- | ---: |
| Parser Cases | 20 |
| Ranking Cases | 12 |
| Safety Cases | 15 |

## Notes

- Benchmarks are synthetic or hand-authored for the reduced MVP scope.
- Ranking evaluation uses structured evidence cases.
- Safety evaluation uses free-text inputs passed through the parser and rule engine.
- These numbers should be refreshed after future parser or CPT changes.
