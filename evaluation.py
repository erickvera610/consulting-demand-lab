"""Rolling-origin selection and untouched final chronological holdout."""
import math, csv
from pathlib import Path

def predict(train, horizon, period, model):
    if len(train) < 2 * period:
        raise ValueError('Two seasons of training required')
    if model == 'seasonal_naive':
        return [train[-period + i % period] for i in range(horizon)]
    log = model == 'log_trend'
    values = [math.log(max(v, 0.001)) for v in train] if log else train
    n = len(values)
    mx = (n - 1) / 2
    my = sum(values) / n
    a = sum(((i - mx) * (v - my) for i, v in enumerate(values))) / sum(((i - mx) ** 2 for i in range(n)))
    b = my - a * mx
    seasonal = [sum((values[i] - a * i - b for i in range(d, n, period))) / len(range(d, n, period)) for d in range(period)]
    out = [a * i + b + seasonal[i % period] for i in range(n, n + horizon)]
    return [math.exp(v) if log else max(0, v) for v in out]

def score(a, b):
    return sum((abs(x - y) for x, y in zip(a, b))) / len(a)

def evaluate(data, period, horizon):
    if len(data) < 8 * period or any((not math.isfinite(v) or v <= 0 for v in data)):
        raise ValueError('Need positive finite data covering eight seasons')
    end = len(data) - horizon
    origins = [end - 3 * horizon, end - 2 * horizon, end - horizon]
    trials = []
    errors = {}
    for model in ['seasonal_naive', 'linear_trend', 'log_trend']:
        folds = []
        residual = []
        for origin in origins:
            prediction = predict(data[:origin], horizon, period, model)
            actual = data[origin:origin + horizon]
            folds.append({'train_end_exclusive': origin, 'validation_end_exclusive': origin + horizon, 'mae': score(actual, prediction)})
            residual.extend((abs(a - b) for a, b in zip(actual, prediction)))
        trials.append({'model': model, 'validation_mae': sum((f['mae'] for f in folds)) / 3, 'folds': folds})
        errors[model] = residual
    chosen = min(trials, key=lambda x: x['validation_mae'])['model']
    pred = predict(data[:end], horizon, period, chosen)
    actual = data[end:]
    base = predict(data[:end], horizon, period, 'seasonal_naive')
    sorted_errors = sorted(errors[chosen])
    radius = sorted_errors[min(len(sorted_errors) - 1, math.ceil(0.8 * (len(sorted_errors) + 1)) - 1)]
    low = [max(0, x - radius) for x in pred]
    high = [x + radius for x in pred]
    return {'selected_model': chosen, 'model_selection': trials, 'mae': score(actual, pred), 'baseline_mae': score(actual, base), 'train_days': end, 'test_days': horizon, 'actual': actual, 'predicted': pred, 'baseline': base, 'lower': low, 'upper': high, 'interval_target': 0.8, 'interval_test_coverage': sum((l <= a <= u for a, l, u in zip(actual, low, high))) / horizon, 'interval_method': 'Absolute residual quantile from earlier validation folds; empirical, not guaranteed coverage', 'test_start_exclusive': end, 'period': period}

def run_evaluation(p):
    dataset = p.get('dataset', 'synthetic')
    if dataset == 'airpassengers':
        with (Path(__file__).parent / 'data' / 'airpassengers.csv').open() as f:
            data = [float(r['value']) for r in csv.DictReader(f)]
        period = 12
        horizon = 12
        unit = 'thousands of passengers per month'
        kind = 'public historical benchmark'
    elif dataset == 'synthetic':
        import random
        rng = random.Random(int(p.get('seed', 42)))
        noise = float(p.get('noise', 5))
        if not 0 <= noise <= 50:
            raise ValueError('Noise must be 0–50')
        data = [max(1, 100 + 0.5 * i + [10, 5, 0, -5, -10, 20, 15][i % 7] + rng.gauss(0, noise)) for i in range(168)]
        period = 7
        horizon = 28
        unit = 'fictional units per day'
        kind = 'synthetic'
    else:
        raise ValueError('Unknown dataset')
    return {**evaluate(data, period, horizon), 'dataset': dataset, 'data_kind': kind, 'unit': unit, 'note': 'Model selected on three earlier folds; final holdout used once. Historical airline data do not represent current demand. Independent consulting project.'}
