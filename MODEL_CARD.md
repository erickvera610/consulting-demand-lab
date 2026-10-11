# Model card: neural demand forecasting

## What a reviewer can verify

[Run the public demo](https://erickvera610.github.io/consulting-demand-lab/model-demo.html). It uses the actual exported trained parameters, without a server account. The Python API uses the same parameters. `test_model.cjs` checks Python/browser numerical parity. Full test metrics and documented errors are in [model-results.json](artifacts/model-results.json), with model SHA-256 and data checksums in [SOURCE.json](data/SOURCE.json).

## Data and experiment

UCI Bike Sharing: 731 real daily observations from Capital Bikeshare, 2011–2012, CC BY 4.0. Attribution: Fanaee-T (2013), DOI [10.24432/C5W894](https://doi.org/10.24432/C5W894). The first 14 days provide history; 717 prediction rows remain.

Chronological split: 430 training, 143 validation, 144 final test days. Compare 9→16→1 and 9→32→1 ReLU MLP regressors using validation MAE, choose 32, then refit train+validation. Scale features and target using only fitting data. Seed 42; CPU training; maximum 500 epochs, no random temporal holdout. At least one candidate reaches the epoch limit, so convergence is not guaranteed. The final loss curve is exported. This is a small neural network, not large-scale deep learning.

Inputs: calendar cycles, elapsed days, previous-day/previous-week counts, and trailing 7/14-day averages. No target-day observed weather or counts split into registered/casual. Forecast at the end of each day for the next day; later test forecasts use already observed earlier test days. This is rolling one-day evaluation, not a fixed-origin forecast of the entire test period.

| Held-out model | MAE (rentals/day) |
|---|---:|
| Repeat same weekday last week | 1218.74 |
| Trained neural network | 1020.32 |
| Trained Ridge comparison | 888.78 |

Neural MAE improves 16.28% versus seasonal repetition. **Ridge wins both validation and this held-out comparison.** Prefer Ridge for this dataset if choosing by measured performance. The neural model remains an inspectable training experiment; complexity does not imply superiority. No claim of state-of-the-art results, employer demand prediction or production readiness.

The complete 144-day test series and ten largest errors are exported, including dates, inputs, truth and predictions. A single city and two years limit generalization. Extreme weather is not represented in the predictors, and can produce large errors. No intervals or causal effects claimed.

## Reproduce and inspect

```bash
python -m pip install -r requirements-model.txt
python train_model.py
python -m unittest discover -v
node test_model.cjs
python model_server.py
```

Open http://127.0.0.1:8001. `POST /api/predict` accepts a JSON object, validates inputs and returns numeric model inference. `GET /health` reports server health. The public Pages demo runs inference in the browser; the Python API is local, not an always-on hosted endpoint. Existing original demos remain available.

GitHub Actions repeats training on Python 3.11/3.12, checks all unit tests and cross-language predictions, then uploads weights/results/source metadata as downloadable artifacts. Data downloads require network access. Floating-point values and optimization can vary across environments; stored exact hashes identify each exported run, not a promise of universal bitwise reproduction.

## Relation to applications

This is an independent, AI-assisted portfolio experiment. No employer affiliation or proprietary employer data. Application documents reviewed privately are not republished.

| Application context | Evidence this project provides | Gap remaining |
|---|---|---|
| DoorDash Software Engineer Intern, requisition 8171041 | Python implementation, validated prediction API, automated unit tests, GitHub CI, executable browser interface | Large-scale distributed operations, production monitoring and deployment are not demonstrated |
| Jump AI Research Engineer – Deep Learning Intern, requisition 8052338 | Explicit training/validation/test protocol, model export, benchmark comparisons and error analysis | No PyTorch/JAX/TensorFlow, CUDA, HPC, large-scale training, transformers, latency-sensitive trading or state-of-the-art research |
| Lilly technology resume previously prepared | Reproducible Python model evaluation and quantitative research communication | Resume is application context, not verified requirements for a specific Lilly vacancy |
| BCG analytics interests discussed | Baseline comparison, model limitations and clear quantitative evidence | No consulting engagement, business impact or employer endorsement claimed |

General Motors is not an active application target following the user's reported rejection. This work supports technical discussion; it does not establish eligibility or guarantee hiring.

## Ownership and interview preparation

Development used AI assistance. Automated daily fictional exercises are separate from these real-data experiments and do not establish manual work history. Before presenting the project, reproduce the experiment, explain the features/splits, inspect a failure and be able to change the implementation. Discuss measured results and remaining gaps precisely.
