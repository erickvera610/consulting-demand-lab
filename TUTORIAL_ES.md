# Tutorial en español: Demand Forecasting Lab

## 1. Qué problema resuelve

Pronosticar significa estimar valores futuros usando solo información anterior. Este proyecto compara tres modelos antes de revisar la prueba final.

## 2. Pruébalo primero

Abre https://erickvera610.github.io/consulting-demand-lab/ . La demo funciona en tu navegador. Cambia un control y compara la salida. Los datos ficticios no son usuarios reales; los ejemplos tampoco representan trabajo realizado para una empresa.

## 3. Instálalo paso a paso

1. Instala Python desde python.org y Git desde git-scm.com.
2. Abre PowerShell y escribe `python --version` y `git --version`.
3. Escribe `git clone https://github.com/erickvera610/consulting-demand-lab.git`.
4. Escribe `cd consulting-demand-lab`.
5. Escribe `python app.py` y mantén abierta la terminal.
6. Abre http://127.0.0.1:8000 y prueba los controles.
7. Detén el servidor con Ctrl+C.

## 4. La secuencia de trabajo

`Historical sequence → rolling-origin validation → model choice → chronological holdout`

**Baseline** es una comparación sencilla: repetir la última temporada. **Rolling origin** significa avanzar el corte temporal: en cada paso se entrena con el pasado y se compara con el período siguiente. La **validación** elige entre repetición estacional, tendencia lineal y tendencia logarítmica. El **holdout** es el último período reservado: no decide qué modelo gana. **MAE** es el promedio de los errores absolutos. Una banda empírica usa errores anteriores; cobertura 75% significa que 9 de los 12 valores estuvieron dentro, aunque el objetivo fuera 80%.

AirPassengers mide miles de pasajeros mensuales, no ventas diarias. Por eso la unidad y la temporada cambian al seleccionar ese dataset.

## 5. Leer el código con calma

Empieza por `core.py` y busca `run`. Después abre el archivo especializado indicado en README. Sigue una sola entrada hasta su salida. Lee las pruebas: cada una describe un comportamiento concreto. Por último, revisa `enhanced.js` para comparar la versión del navegador.

## 6. Reproducir los resultados

```bash
python -m unittest discover -v
node test_enhanced.cjs
python benchmark.py
```

Abre `benchmark-results.json` y compara su resumen con `CASE_STUDY.md`. El reporte incluye una hora real de ejecución. Los experimentos con semillas repetidas muestran varios resultados; no escogemos solo el mejor. Las métricas sintéticas de JavaScript pueden diferir de Python.

## 7. Tu siguiente mejora personal

Añade un benchmark público más reciente con su fuente y licencia. Compara más horizontes, y reserva un período exclusivo para calibrar intervalos.

```bash
git switch -c feature/my-improvement
# Edita código y ejecuta las pruebas
git add .
git commit -m "Describe the actual behavior change"
git push -u origin feature/my-improvement
```

Abre un pull request y explica problema, solución, resultado y límite. Se usó asistencia de IA para construir esta base. En una entrevista distingue lo que recibiste, lo que estudiaste y lo que realmente cambiaste.

## 8. Practicar la entrevista

- What problem does this application solve?
- Which data are available when the prediction is made?
- What is the simplest baseline?
- How did you avoid data leakage or inconsistent state?
- Which result surprised you?
- What failure case remains?
- What did you personally improve?

Primero responde en español. Después prepara cuatro frases cortas en inglés: problema, método, resultado y limitación. Usa solo resultados documentados.
