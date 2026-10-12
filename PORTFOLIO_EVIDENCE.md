# Portfolio Evidence

This page summarizes the strongest recruiter-facing evidence in this repository and separates measured results from broader claims.

## Real data

- Primary real-data experiment: **UCI Bike Sharing Dataset**.
- 731 daily observations from Capital Bikeshare covering 2011–2012.
- The first 14 days are used to construct lag/history features; 717 prediction rows remain.
- Chronological split: **430 training / 143 validation / 144 final test days**.
- The final test period is not used for model selection.

## Forecasting task

The model predicts next-day bike-rental demand using only information available before the target day:

- calendar-cycle features,
- elapsed time,
- previous-day count,
- previous-week count,
- trailing 7-day average,
- trailing 14-day average.

Target-day observed weather and same-day registered/casual counts are excluded to reduce leakage.

## Models compared

- Seasonal baseline: repeat the same weekday from the previous week.
- Ridge regression.
- Small ReLU multilayer perceptrons: `9→16→1` and `9→32→1`.

The neural-network width is selected with validation MAE, then the selected model is refit on train + validation data. Scaling is fitted only on the data available to each fitting stage.

## Held-out results

| Model | Final test MAE |
|---|---:|
| Repeat same weekday last week | **1218.74 rentals/day** |
| Neural network | **1020.32 rentals/day** |
| Ridge regression | **888.78 rentals/day** |

The neural model improves MAE by **16.28%** relative to the seasonal baseline, but **Ridge performs best** on the held-out test period. This is an important result: model complexity was not treated as evidence of superiority.

## Additional public forecasting evidence

The repository also includes an AirPassengers benchmark using rolling-origin validation and a final chronological holdout.

- Selected model: linear trend + seasonality.
- Holdout MAE: **37.3805 thousand passengers/month**.
- Seasonal baseline MAE: **47.8333 thousand passengers/month**.
- Empirical interval coverage: **0.75** on the 12-month holdout.

This benchmark is historical and small, so it demonstrates forecasting workflow rather than production-scale demand planning.

## Evidence a recruiter can inspect

1. `train_model.py` — real-data training pipeline.
2. `MODEL_CARD.md` — experiment design, metrics, limitations, and model comparison.
3. `artifacts/model-results.json` — held-out predictions, metrics, and largest errors.
4. `data/SOURCE.json` — dataset source, attribution, and checksums.
5. `model-demo.html` — browser inference using exported trained parameters.
6. `model_server.py` — local Python inference API.
7. `test_model.cjs` — Python/browser numerical parity.
8. GitHub Actions — automated training and test execution.

## Engineering and ML skills demonstrated

Python, supervised regression, neural-network training, Ridge regression, temporal feature engineering, chronological validation, leakage prevention, baseline comparison, model selection, model export, inference APIs, reproducibility, unit testing, CI, and error analysis.

## Important limitations

- Only one city and two years of bike-sharing data are used.
- The neural network is small and CPU-trained; this is not large-scale deep learning.
- Extreme weather is not represented directly in the predictor set.
- The test protocol is rolling one-day-ahead forecasting, not a fixed-origin long-horizon forecast.
- No claim is made about causal impact, state-of-the-art forecasting, or production deployment.

## Recruiter takeaway

The strongest evidence in this project is not that a neural network was trained. It is that multiple models were compared under a chronological protocol, leakage was explicitly controlled, a simple Ridge model was accepted as the winner when it performed best, and all results can be reproduced and inspected.

That combination demonstrates practical model judgment in addition to implementation skill.
