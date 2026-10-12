# Demand Forecasting Lab

> **Recruiter quick view:** real historical demand data, chronological evaluation, seasonal baseline, Ridge vs neural-network comparison, PyTorch extension, model export, browser inference, error analysis, tests, and CI. Start with [RECRUITER_OVERVIEW.md](RECRUITER_OVERVIEW.md), [PORTFOLIO_EVIDENCE.md](PORTFOLIO_EVIDENCE.md), [MODEL_CARD.md](MODEL_CARD.md), and the [interactive model demo](https://erickvera610.github.io/consulting-demand-lab/model-demo.html).

## Real-data next-day demand experiment

The main trained-model experiment uses the **UCI Bike Sharing Dataset** with 731 real daily observations from Capital Bikeshare. After 14 days of history for lag features, 717 prediction rows remain.

Chronological split:

- Train: **430 days**
- Validation: **143 days**
- Final test: **144 days**

Models compared:

- repeat-same-weekday seasonal baseline,
- Ridge regression,
- small ReLU MLPs.

Held-out MAE:

| Model | MAE (rentals/day) |
|---|---:|
| Seasonal baseline | **1218.74** |
| scikit-learn neural network | **1020.32** |
| Ridge regression | **888.78** |

The neural model improves over the seasonal baseline, but **Ridge wins the measured held-out comparison**. The project therefore emphasizes model judgment rather than assuming a more complex model is better.

## PyTorch extension

`pytorch_demand.py` adds a separate PyTorch MLP benchmark under the same chronological 60/20/20 discipline.

```bash
python -m pip install -r requirements-pytorch.txt
python pytorch_demand.py
```

The script selects hidden width using validation MAE and writes the held-out result to `artifacts/pytorch-demand-results.json`. Do not quote that metric until the script has been run in the current environment.

## Features and leakage control

Inputs include:

- weekday and month cycles,
- elapsed days,
- previous-day count,
- previous-week count,
- trailing 7-day average,
- trailing 14-day average.

Target-day observed weather and same-day casual/registered counts are excluded. The task is rolling one-day-ahead forecasting, not a fixed-origin multi-month forecast.

## Additional forecasting benchmark

The repository also preserves an AirPassengers experiment using rolling-origin validation and a final chronological holdout.

| Measurement | Result |
|---|---:|
| Selected model | linear trend + seasonality |
| Holdout MAE | **37.3805** thousand passengers/month |
| Seasonal baseline MAE | **47.8333** |
| Empirical interval coverage | **0.75** |
| Test months | **12** |

This small historical benchmark demonstrates forecasting workflow, not production demand planning.

## Demo and reproducibility

**[Interactive trained-model demo](https://erickvera610.github.io/consulting-demand-lab/model-demo.html)** · [Model card](MODEL_CARD.md) · [Actions](https://github.com/erickvera610/consulting-demand-lab/actions)

```bash
python -m pip install -r requirements-model.txt
python train_model.py
python -m unittest discover -v
node test_model.cjs
python model_server.py
```

The browser and Python API use exported parameters; parity tests verify the numerical path.

## Skills demonstrated

Python, scikit-learn, PyTorch, time-series feature engineering, chronological splitting, neural networks, Ridge regression, baselines, validation-based model selection, leakage control, model export, inference APIs, error analysis, tests, and CI.

## Key files

- `train_model.py` — real-data Ridge/MLP comparison.
- `pytorch_demand.py` — PyTorch neural benchmark.
- `MODEL_CARD.md` — protocol, metrics, largest errors, and limitations.
- `artifacts/model-results.json` — held-out predictions and errors.
- `RECRUITER_OVERVIEW.md` — recruiter review path and screenshot checklist.
- `PORTFOLIO_EVIDENCE.md` — evidence summary.

## Limitations

The real-data experiment covers one bike-sharing system and two historical years. The neural networks are small CPU models, not large-scale deep learning. Extreme weather is not directly represented in the feature set. No causal, state-of-the-art, or production-readiness claim is made.

## Authorship

Independent AI-assisted learning project in Erik Vera's portfolio. No employer affiliation or proprietary employer data. Code is MIT licensed; third-party data attribution is documented separately.
