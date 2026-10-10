# Consulting Demand Lab

BCG-sector-inspired demand forecasting with chronological holdout, weekday effects, MAE and a baseline.

An AI-assisted educational portfolio project prepared for Erik Vera's internship learning. This is a working prototype, not production software. Authorship and skills should be represented based on what you can explain and change independently.

## Public demo

[Open browser demo](https://erickvera610.github.io/consulting-demand-lab/). Visitors can run examples on their device without write access to this repository.

## Run in two minutes

Requires Python 3.11 or newer; no pip dependencies.

```bash
git clone https://github.com/erickvera610/consulting-demand-lab.git
cd consulting-demand-lab
python app.py
```

Open http://127.0.0.1:8000. On Windows, use `py app.py` if `python` is unavailable. Stop with Ctrl+C. Run `python -m unittest discover -v` to execute tests.

## Architecture

- `index.html`: responsive accessible interface; renders output with textContent.
- `app.py`: local HTTP service, `/health`, and validated JSON POST `/api/run`.
- `core.py`: domain logic separated from transport and presentation.
- `test_core.py`: deterministic behavior and failure cases.
- `.github/workflows/tests.yml`: Python 3.11 and 3.12 CI.
- `TUTORIAL_ES.md`: beginner Spanish guide and interview practice.

## API

POST a JSON object to `/api/run`; inputs are the same fields used by the interface. Responses are JSON. Invalid inputs return 400; unknown paths return 404. GET `/health` returns `{"status":"ok"}`.

## Design and limits

Pronosticar demanda ayuda a planear recursos. Ajusto una tendencia lineal con 84 días y calculo efectos por día de la semana usando solo entrenamiento. Los siguientes 28 días se reservan para prueba. MAE es el promedio del error absoluto. Comparo con repetir la última semana; si no supera ese baseline, el modelo no aporta suficiente valor.

The built-in HTTP server is for a local demonstration. There is no authentication, rate limiting, or public production deployment. Never enter personal application records on a publicly exposed demo. Bind to localhost by default. For Codespaces only, run `HOST=0.0.0.0 python app.py` and keep the forwarded port private; usage may consume your GitHub quota.

## Review and contribution workflow

Create a feature branch, make one small change, run the tests, commit it, push the branch, and open a pull request. Explain the change and validation. Do not fabricate collaboration or commit history. Suggested first improvement: add a new input option with one behavior test and update this README.

## References

- https://docs.python.org/3/library/http.server.html
- https://docs.github.com/en/actions/tutorials/build-and-test-code/python

License: MIT.

## Daily practical exercises

A daily GitHub Actions job runs one dated fictional scenario and saves inputs and outputs in `exercises/`. Read [Spanish daily guide](EJERCICIOS_DIARIOS_ES.md). Commits are authored by github-actions[bot].
