# Ejercicios prácticos diarios

Una vez al día GitHub Actions ejecuta `python daily_exercise.py` con datos ficticios. La semilla deriva de la fecha UTC; los controles o los datos cambian cada día. `exercises/AAAA-MM-DD/result.json` contiene entrada, salida y hora real de ejecución; `samples/latest.json` contiene la entrada más reciente.

Los resultados se guardan con el autor `github-actions[bot]`. Esto documenta ejercicios ejecutados mediante script; no representa usuarios reales ni desarrollo manual diario. Ejecutar una segunda vez el mismo día conserva el resultado existente. Las demos del navegador se ejecutan localmente y no escriben en GitHub.

## Cómo practicar

1. Abre el último `result.json` y predice la salida leyendo la entrada.
2. Ejecuta `python daily_exercise.py` localmente después de instalar las dependencias indicadas en README.
3. Lee `core.py` (o `app.py` en Mercado) y explica la métrica o el cambio de estado.
4. Para estudiar otra entrada el mismo día, importa `core.run` en Python; el historial diario conserva un único resultado por fecha.
5. Abre Actions → Ejercicios prácticos diarios para revisar la ejecución. Puedes usar Run workflow para recuperar un día si el horario se retrasa.

El horario es diario por la mañana en Indianápolis (12:17–12:37 UTC según repositorio). GitHub puede retrasar ejecuciones; no es un servicio con garantía de puntualidad. Datos exclusivamente ficticios, sin llamadas a servicios de trading, empresas o vehículos.
