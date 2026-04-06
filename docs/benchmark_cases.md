# Benchmark Cases

The tracked benchmark cases for the MVP now live in:

- `/Users/adityaghosh/Desktop/CS3263/Project/elderly-care-mvp/config/benchmark_cases.yaml`

They are divided into:

- parser cases: free-text inputs with expected labeled evidence
- ranking cases: structured evidence with expected top-1 and acceptable top-2 conditions
- safety cases: free-text inputs with expected escalation behavior

Current benchmark coverage includes:

- dehydration-like benign cases
- hypoglycemia-like benign cases
- viral-pattern benign cases
- medication-side-effect benign cases
- negation cases
- chest pain, fainting, fall-plus-dizziness, and severe-confusion urgent cases

To regenerate the summary artifacts after changing parser rules, CPTs, or safety logic, run:

```bash
python3 -m src.eval
```
