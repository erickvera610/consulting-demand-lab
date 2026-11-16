"""Validated dated-history adapter for the existing historical MLP experiment."""
import argparse
import datetime as dt
import json
import math
from pathlib import Path
from model import load_model, predict

# Fixed origin of the existing exported model's elapsed_days feature.
ORIGIN = dt.date(2011, 1, 1)
FEATURES = ['weekday_sin','weekday_cos','month_sin','month_cos','elapsed_days',
            'lag_1_day','lag_7_days','past_7_day_mean','past_14_day_mean']


def parse_date(value):
    if not isinstance(value, str):
        raise ValueError('Dates must be YYYY-MM-DD strings')
    try:
        result = dt.date.fromisoformat(value)
    except ValueError:
        raise ValueError('Dates must be YYYY-MM-DD strings') from None
    if result.isoformat() != value:
        raise ValueError('Dates must be YYYY-MM-DD strings')
    return result


def build_features(target_date, history):
    target = parse_date(target_date)
    if target < ORIGIN + dt.timedelta(days=14):
        raise ValueError('Target precedes the model history window')
    if not isinstance(history, list) or len(history) != 14:
        raise ValueError('Supply exactly the 14 calendar days before the target')
    values = {}
    for row in history:
        if not isinstance(row, dict) or set(row) != {'date', 'count'}:
            raise ValueError('Each history row requires only date and count')
        date = parse_date(row['date'])
        count = row['count']
        if isinstance(count, bool) or not isinstance(count, (int, float)) or not math.isfinite(count) or count < 0:
            raise ValueError('Counts must be finite nonnegative numbers')
        if date >= target:
            raise ValueError('Target-day and future observations are not allowed')
        if date in values:
            raise ValueError('Duplicate history date')
        values[date] = float(count)
    dates = [target-dt.timedelta(days=i) for i in range(14, 0, -1)]
    if set(values) != set(dates):
        raise ValueError('History must contain every preceding calendar day')
    counts = [values[d] for d in dates]
    return [math.sin(2*math.pi*target.weekday()/7), math.cos(2*math.pi*target.weekday()/7),
            math.sin(2*math.pi*target.month/12), math.cos(2*math.pi*target.month/12),
            (target-ORIGIN).days, counts[-1], counts[-7],
            sum(counts[-7:])/7, sum(counts)/14]


def forecast(payload):
    if not isinstance(payload, dict) or set(payload) != {'target_date', 'history'}:
        raise ValueError('Payload requires only target_date and history')
    model = load_model()
    if model.get('task') != 'demand' or model.get('features') != FEATURES:
        raise ValueError('Incompatible model feature schema')
    x = build_features(payload['target_date'], payload['history'])
    return {'target_date': payload['target_date'], **predict({'features': x}, model),
            'features': dict(zip(FEATURES, x)),
            'limitations': 'Historical MLP experiment, not a current operational forecast. Ridge outperformed this MLP on the recorded test set.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    try:
        result = forecast(json.loads(args.input.read_text()))
    except (ValueError, OSError) as error:
        parser.exit(2, str(error)+'\n')
    print(json.dumps(result, indent=2, allow_nan=False))
