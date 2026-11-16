"""Reproduce the dated adapter against all archived held-out forecasts."""
import csv
import io
import json
import urllib.request
import zipfile
from forecast_history import build_features, forecast
from model import ROOT, digest
import numpy as np


def main():
    path=ROOT/'data/day.csv'
    if not path.exists():
        with urllib.request.urlopen('https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip',timeout=60) as response:
            archive=zipfile.ZipFile(io.BytesIO(response.read()))
        path.write_bytes(archive.read('day.csv'))
    source=json.loads((ROOT/'data/SOURCE.json').read_text())
    if digest(path)!=source['sha256']:raise ValueError('Dataset checksum mismatch')
    with path.open() as stream: rows=list(csv.DictReader(stream))
    positions={r['dteday']:i for i,r in enumerate(rows)}
    report=json.loads((ROOT/'artifacts/model-results.json').read_text())
    checked=[]
    for example in report['examples']:
        i=positions[example['date']]
        payload={'target_date':example['date'],'history':[{'date':r['dteday'],'count':int(r['cnt'])} for r in rows[i-14:i]]}
        x=build_features(payload['target_date'],payload['history'])
        np.testing.assert_allclose(x, example['features'], rtol=0, atol=1e-10)
        result=forecast(payload)
        np.testing.assert_allclose(result['prediction'],example['prediction'],rtol=0,atol=1e-8)
        checked.append({'date':example['date'],'prediction':result['prediction'],'absolute_difference':abs(result['prediction']-example['prediction'])})
        if len(checked)==1:
            (ROOT/'samples/history-example.json').write_text(json.dumps(payload,indent=2)+'\n')
            (ROOT/'artifacts/history-example-result.json').write_text(json.dumps(result,indent=2)+'\n')
    result={'checked_forecasts':len(checked),'max_absolute_prediction_difference':max(r['absolute_difference'] for r in checked),
            'dataset_sha256':digest(path),'model_sha256':digest(ROOT/'artifacts/model.json'),
            'interpretation':'Parity with the archived MLP, not an accuracy improvement.', 'rows':checked}
    (ROOT/'artifacts/history-validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}))

if __name__=='__main__':main()
