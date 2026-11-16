# Forecast from dated history

The original model API accepts nine numerical features in a prescribed order. A caller could put the wrong day's demand into a lag or compute a mean over an incomplete calendar window. The new `forecast_history.py` CLI constructs those features from an explicit target date and exactly 14 preceding daily observations.

## Run the included real-data example

```bash
python -m pip install -r requirements-model.txt
python forecast_history.py samples/history-example.json
python -m unittest discover -v
python validate_history.py
node test_model.cjs
node test_demo.cjs
node test_enhanced.cjs
```

The sample is derived from the public UCI Bike Sharing day.csv (see data/SOURCE.json for attribution). It contains dates July 27–August 9, 2012, and forecasts August 10, 2012. No target-day observation is an input. The sample and existing exported model permit offline inference after dependencies are installed; the full parity validator downloads the source CSV if absent and checks its SHA-256.

Measured output with the checked-in MLP:

- Prior-day demand: 7,286 rentals.
- Prior-week demand: 7,175 rentals.
- Prior-seven-day average: 6,938.428571 rentals.
- Prediction: **6,668.674175 rentals**.
- Actual target-day demand, used only for comparison: **5,786 rentals**.
- Absolute error on this example: **882.674175 rentals**.

This example was selected as the first archived held-out forecast, not for its error. It is illustrative, not an aggregate accuracy result.

## Contract

Input JSON has exactly `target_date` and `history`. Every history row has exactly `date` and `count`. Dates use YYYY-MM-DD. Counts must be finite, nonnegative JSON numbers; booleans are rejected. Records may arrive in any order. Duplicate dates, missing days, stale windows, target-day/future observations and incompatible model feature order are rejected with an error. The CLI exits with code 2 for invalid input. It does not fill missing demand with zero or silently ignore future rows.

The calendar origin is fixed to 2011-01-01, matching the existing exported model. Changing the origin for a new dataset would change elapsed_days and requires a matching model. This adapter is for the repository's historical model, not an interchangeable forecasting service. Existing raw-feature API behavior is unchanged.

## Validation and limits

`validate_history.py` reconstructs every one of the **144 archived held-out forecasts** from dated raw history and compares both feature vectors and predictions. Maximum absolute prediction difference on the local run: **0.0**. The report records all dates, differences, source hash and model hash in artifacts/history-validation.json. No retraining was performed for this local validation.

All **17 Python tests passed**, including five new test methods covering known lags and averages, order independence, no input mutation, future observations, missing/duplicate/stale dates and invalid values. Python/browser model parity and both other JavaScript suites passed locally. CI now runs the history validator; remote CI success is not asserted.

The adapter validates dates and values, not whether observations were truly available or later revised. It does not make arbitrary future dates or other bike systems in-distribution. The historical MLP still loses to Ridge in the recorded aggregate test comparison. No improvement in model accuracy, causal claim or current operational reliability is implied. Independent AI-assisted portfolio extension.
