"""One dated practical exercise, with fictional data and transparent script execution."""
import json, random, tempfile, os
from pathlib import Path
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parent
import sys
sys.path.insert(0, str(ROOT))
PROJECT = 'consulting-demand-lab'
NOW = datetime.now(timezone.utc)
DAY = NOW.date().isoformat()
DEST = ROOT / 'exercises' / DAY / 'result.json'

def exercise():
    seed = int(DAY.replace('-', ''))
    rng = random.Random(seed)
    if PROJECT == 'mercado-aprende':
        from app import create_app
        with tempfile.TemporaryDirectory() as tmp:
            app = create_app({'TESTING': True, 'SECRET_KEY': 'fictional-isolated-exercise', 'DATABASE': str(Path(tmp) / 'market.db')})
            seller, buyer = (app.test_client(), app.test_client())

            def post(client, path, data):
                client.get('/login')
                with client.session_transaction() as session:
                    token = session['csrf']
                return client.post(path, data={**data, 'csrf': token})
            for client, user in [(seller, 'fictional_seller'), (buyer, 'fictional_buyer')]:
                assert post(client, '/register', {'username': user, 'password': 'fictional-password'}).status_code == 302
                assert post(client, '/login', {'username': user, 'password': 'fictional-password'}).status_code == 302
            payload = {'title': f'Fictional product {DAY}', 'category': 'Libros', 'condition': 'Usado', 'price': str(rng.randint(10, 100)), 'description': 'Daily fictional exercise product'}
            assert post(seller, '/sell', payload).status_code == 302
            assert post(buyer, '/items/1/buy', {}).status_code == 302
            output = {'published': True, 'purchased': True, 'history_visible': payload['title'].encode() in buyer.get('/account').data}
            assert output['history_visible']
    else:
        import core
        if PROJECT == 'internship-tracker':
            payload = {'company': f'Fictional Company {DAY}', 'role': rng.choice(['Software Intern', 'ML Intern', 'Data Intern']), 'status': rng.choice(core.STATUSES), 'deadline': f'{NOW.year + 1}-03-{rng.randint(1, 28):02}'}
        elif PROJECT == 'ml-model-lab':
            payload = {'threshold': round(rng.uniform(0.1, 0.9), 3)}
        elif PROJECT == 'research-search':
            payload = {'query': rng.choice(['machine learning', 'Sobel convolution', 'SQLite APIs', 'software tests', 'graph route'])}
        elif PROJECT == 'vision-playground':
            payload = {'mode': rng.choice(['original', 'blur', 'edges']), 'image': [[rng.randint(0, 255) for _ in range(16)] for _ in range(16)]}
        elif PROJECT == 'route-planner':
            payload = {'blocked': [[x, y] for x in range(1, 11) for y in range(1, 11) if rng.random() < 0.18]}
        elif PROJECT == 'trading-strategy-lab':
            payload = {'seed': seed, 'window': rng.randint(2, 30), 'cost_bps': rng.randint(0, 30)}
        elif PROJECT == 'media-content-lab':
            payload = {'seed': seed, 'min_views': rng.randint(100, 3000)}
        elif PROJECT == 'road-vision-lab':
            payload = {'seed': seed, 'noise': rng.randint(0, 15)}
        elif PROJECT == 'consulting-demand-lab':
            payload = {'seed': seed, 'noise': rng.randint(0, 30)}
        elif PROJECT == 'incident-response-lab':
            payload = {'seed': seed, 'count': rng.randint(10, 25)}
        else:
            raise ValueError('Unknown project')
        if PROJECT in ['road-vision-lab', 'media-content-lab', 'consulting-demand-lab', 'ml-model-lab']:
            payload['seed'] = seed
            payload['mode'] = {'road-vision-lab': 'pixels', 'media-content-lab': 'model', 'consulting-demand-lab': 'evaluate', 'ml-model-lab': 'evaluate'}[PROJECT]
        with tempfile.TemporaryDirectory() as tmp:
            previous = os.getcwd()
            os.chdir(tmp)
            try:
                output = core.transform(payload['image'], payload['mode']) if PROJECT == 'vision-playground' else core.run(payload)
            finally:
                os.chdir(previous)
    return {'project': PROJECT, 'date_utc': DAY, 'executed_at_utc': NOW.isoformat(), 'data_kind': 'fictional/synthetic', 'execution_method': 'Python script', 'seed': seed, 'input': payload, 'output': output, 'completed': True}
if __name__ == '__main__':
    if DEST.exists():
        print(f'{PROJECT}: exercise already recorded for {DAY}')
    else:
        result = exercise()
        DEST.parent.mkdir(parents=True, exist_ok=True)
        DEST.write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
        latest = ROOT / 'samples' / 'latest.json'
        latest.parent.mkdir(exist_ok=True)
        latest.write_text(json.dumps(result['input'], indent=2), encoding='utf-8')
        print(f'{PROJECT}: practical exercise completed for {DAY}')
