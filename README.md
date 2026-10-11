# Demand Forecasting Lab

The original single-model synthetic demonstration now compares three forecasting candidates and includes a public historical benchmark. A final year remains untouched while three earlier folds select the model.

**[Open the live demo](https://erickvera610.github.io/consulting-demand-lab/)** · [Spanish tutorial](TUTORIAL_ES.md) · [Case study](CASE_STUDY.md) · [Measured results](benchmark-results.json)

## Understand it in one minute

Historical sequence → rolling-origin validation → model choice → chronological holdout

Seasonal repetition is the baseline. Additive trend plus seasonality and log trend plus seasonality provide interpretable alternatives. Forecast selection minimizes validation MAE. An absolute-residual quantile supplies an empirical interval; actual final-holdout coverage is reported even when it is below target.

## Measured evidence

Reproduced with Python by `python benchmark.py`. Execution timestamp is recorded in the JSON report. Synthetic JavaScript values may differ because the random generator differs.

| Measurement | Result |
|---|---|
| public dataset | AirPassengers |
| selected model | linear_trend |
| holdout mae | 37.3805 |
| seasonal baseline mae | 47.8333 |
| interval coverage | 0.7500 |
| unit | thousands of passengers per month |
| test months | 12 |

## Run locally

Python 3.11 or 3.12, standard library only. No API keys.

```bash
git clone https://github.com/erickvera610/consulting-demand-lab.git
cd consulting-demand-lab
python app.py
```

Open http://127.0.0.1:8000. Stop with Ctrl+C. The public browser demo requires no installation.

## Reproduce and inspect

```bash
python -m unittest discover -v
node test_enhanced.cjs
python benchmark.py
python daily_exercise.py
```

Use `core.run({"mode":"evaluate","dataset":"airpassengers"})` for the public monthly benchmark, or `core.run({"mode":"evaluate","dataset":"synthetic","seed":42,"noise":5})` for daily fictional exercises.

## Read the source

- `core.py`: public algorithm entry point and preserved original exercise.
- `evaluation.py`: featured implementation.
- `enhanced.js`: browser implementation, readable without a build system.
- `app.py`: localhost HTTP API.
- `test_*.py` and `test_enhanced.cjs`: behavior and edge cases.
- `benchmark.py`: evidence generator.

## Limitations

AirPassengers is historical airline demand, not current customer sales. Months are serially dependent. Only three folds and twelve holdout observations are available. Interval coverage is empirical and not guaranteed. Model selection and interval calibration share validation folds; a separate calibration period would strengthen the method.

## Daily practical exercises

One dated fictional scenario runs daily through GitHub Actions. `exercises/YYYY-MM-DD/result.json` preserves inputs and outputs; `samples/latest.json` holds the latest input. Bot-authored report commits document script execution, not manual daily development. [Daily Spanish guide](EJERCICIOS_DIARIOS_ES.md).

## Authorship and relevance

Independent AI-assisted learning project in Erik Vera's portfolio. No affiliation with FOX, Tesla or BCG. The documentation distinguishes supplied implementation from improvements the learner actually makes. Code is MIT licensed; third-party data provenance is documented separately.

## Featured portfolio

- [Road Vision Lab](https://github.com/erickvera610/road-vision-lab)
- [Demand Forecasting Lab](https://github.com/erickvera610/consulting-demand-lab)
- [Media Prediction Lab](https://github.com/erickvera610/media-content-lab)
- [Classification Evaluation Lab](https://github.com/erickvera610/ml-model-lab)
- [Incident Workflow Lab](https://github.com/erickvera610/incident-response-lab)

## Trained model with real data

[Interactive model demo](https://erickvera610.github.io/consulting-demand-lab/model-demo.html) · [Model card](MODEL_CARD.md) · [Training and tests](https://github.com/erickvera610/consulting-demand-lab/actions)

Install `pip install -r requirements-model.txt`, run `python train_model.py`, then `python -m unittest discover -v` and `node test_model.cjs`. Run `python model_server.py` for the connected Python inference API at http://127.0.0.1:8001.

The original demonstration remains available. This new experiment trains on downloaded public data with checksum verification and separate validation/test partitions. Exported weights execute in the browser and Python API; see the model card for limitations and the exact relation to internship skills.
