"""Reproduce the measured case study without cherry-picking a single seed."""
import json, tempfile
from pathlib import Path
from datetime import datetime, timezone
import core
ROOT = Path(__file__).parent
PROJECT = 'consulting-demand-lab'

def benchmark():
    rows = []
    if PROJECT == 'road-vision-lab':
        for seed in range(10):
            r = core.run({'mode': 'pixels', 'seed': seed, 'noise': 10})
            rows.append({'seed': seed, 'detected': r['detected'], 'width_error_px': r['synthetic_width_error_px'], 'left_inlier_ratio': r['left']['inlier_ratio'] if r['left'] else None})
        blank = core.run({'image': [[0] * 64 for _ in range(48)]})
        summary = {'detected_scenes': sum((r['detected'] for r in rows)), 'scene_count': 10, 'mean_width_error_px': sum((r['width_error_px'] for r in rows if r['width_error_px'] is not None)) / sum((r['width_error_px'] is not None for r in rows)), 'blank_image_detected': blank['detected']}
    elif PROJECT == 'media-content-lab':
        for seed in range(5):
            r = core.run({'mode': 'model', 'seed': seed})
            rows.append({'seed': seed, 'test_mae': r['test_mae'], 'baseline_mae': r['baseline_mae'], 'selected_ridge': r['selected_ridge']})
        summary = {'mean_test_mae': sum((r['test_mae'] for r in rows)) / 5, 'mean_baseline_mae': sum((r['baseline_mae'] for r in rows)) / 5, 'seeds_beating_baseline': sum((r['test_mae'] < r['baseline_mae'] for r in rows))}
    elif PROJECT == 'consulting-demand-lab':
        r = core.run({'mode': 'evaluate', 'dataset': 'airpassengers'})
        rows.append(r)
        summary = {'public_dataset': 'AirPassengers', 'selected_model': r['selected_model'], 'holdout_mae': r['mae'], 'seasonal_baseline_mae': r['baseline_mae'], 'interval_coverage': r['interval_test_coverage'], 'unit': r['unit'], 'test_months': r['test_days']}
    elif PROJECT == 'ml-model-lab':
        for seed in range(5):
            r = core.run({'mode': 'evaluate', 'seed': seed})
            rows.append({'seed': seed, **r['metrics'], 'selected_threshold': r['selected_threshold'], 'baseline_accuracy': r['baseline_accuracy']})
        summary = {'mean_roc_auc': sum((r['roc_auc'] for r in rows)) / 5, 'mean_f1': sum((r['f1'] for r in rows)) / 5, 'mean_brier_score': sum((r['brier_score'] for r in rows)) / 5}
    elif PROJECT == 'incident-response-lab':
        from store import IncidentStore, Conflict
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'incidents.db'
            store = IncidentStore(path)
            r = store.create('Fictional API outage', 'API', 'High')
            first = store.move(r['id'], 'Investigating', 1, 'first')
            repeat = store.move(r['id'], 'Investigating', 1, 'first')
            stale = False
            try:
                store.move(r['id'], 'Resolved', 1, 'stale')
            except Conflict:
                stale = True
            store.move(r['id'], 'Resolved', 2, 'resolve')
            reopened = IncidentStore(path).list()[0]
            summary = {'retry_does_not_duplicate': len(repeat['history']) == 2, 'stale_write_rejected': stale, 'persisted_state_after_reopen': reopened['state'], 'events_after_resolution': len(reopened['history'])}
            rows = [reopened]
    else:
        raise ValueError(PROJECT)
    return {'project': PROJECT, 'executed_at_utc': datetime.now(timezone.utc).isoformat(), 'execution_method': 'Python script', 'summary': summary, 'runs': rows, 'limitations': 'Reproducible prototype evidence, not employer affiliation or production certification.'}
if __name__ == '__main__':
    result = benchmark()
    (ROOT / 'benchmark-results.json').write_text(json.dumps(result, indent=2, allow_nan=False))
    print(json.dumps(result['summary']))
