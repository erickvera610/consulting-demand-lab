# Recruiter Quick View

## What this project proves

This repository demonstrates next-day demand forecasting on real public data with chronological evaluation, explicit baselines, neural-network and Ridge comparisons, reproducible artifacts, and now a separate PyTorch implementation.

## Best evidence to inspect first

1. `MODEL_CARD.md` — experiment design and held-out comparisons.
2. `artifacts/model-results.json` — final test predictions and largest errors.
3. `pytorch_demand.py` — PyTorch MLP benchmark using the same chronological protocol.
4. `train_model.py` — scikit-learn MLP and Ridge comparison.
5. `model-demo.html` — browser inference with exported parameters.
6. GitHub Actions — automated training/tests.

## Skills shown

Python, scikit-learn, PyTorch, time-series feature engineering, chronological train/validation/test splitting, neural networks, Ridge regression, baseline comparison, leakage control, error analysis, APIs, model export, and CI.

## Important interpretation

The strongest result is that Ridge beats the neural model on the existing held-out comparison. The project therefore demonstrates model judgment rather than assuming a deeper model is automatically better.

## Recommended interview demo

Run:

```bash
python -m pip install -r requirements-pytorch.txt
python train_model.py
python pytorch_demand.py
```

Compare the seasonal baseline, Ridge, scikit-learn MLP, and PyTorch MLP. Explain why chronology matters and why target-day weather is excluded.

## Screenshot/result checklist

Capture:

- model-comparison table,
- selected architecture and validation metric,
- a worst-error example,
- browser prediction demo,
- PyTorch held-out result JSON.

Do not present the neural result as the winner unless the measured evaluation supports that claim.
