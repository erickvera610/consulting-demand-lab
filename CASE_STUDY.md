# Case study: Demand Forecasting Lab

## 1. Problem and intended user

The original single-model synthetic demonstration now compares three forecasting candidates and includes a public historical benchmark. A final year remains untouched while three earlier folds select the model.

## 2. Data and information flow

Historical sequence → rolling-origin validation → model choice → chronological holdout

## 3. Why these choices

Seasonal repetition is the baseline. Additive trend plus seasonality and log trend plus seasonality provide interpretable alternatives. Forecast selection minimizes validation MAE. An absolute-residual quantile supplies an empirical interval; actual final-holdout coverage is reported even when it is below target.

## 4. Reproducible evidence

| Measurement | Result |
|---|---|
| public dataset | AirPassengers |
| selected model | linear_trend |
| holdout mae | 37.3805 |
| seasonal baseline mae | 47.8333 |
| interval coverage | 0.7500 |
| unit | thousands of passengers per month |
| test months | 12 |

Generated at 2026-10-10T18:37:09.393640+00:00 by the Python benchmark. Read every run in [benchmark-results.json](benchmark-results.json). These results apply only to the documented benchmark. No production performance claim is made.

## 5. What could go wrong

AirPassengers is historical airline demand, not current customer sales. Months are serially dependent. Only three folds and twelve holdout observations are available. Interval coverage is empirical and not guaranteed. Model selection and interval calibration share validation folds; a separate calibration period would strengthen the method.

## 6. Next substantive improvement

Añade un benchmark público más reciente con su fuente y licencia. Compara más horizontes, y reserva un período exclusivo para calibrar intervalos.

Open an issue, create a branch, implement the improvement, run the checks, and explain the change in a pull request. Do not describe automated report commits as personal code development.
