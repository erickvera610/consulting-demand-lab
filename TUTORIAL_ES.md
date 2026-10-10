# Tutorial en español: Consulting Demand Lab

## 1. Qué hace y por qué existe

BCG-sector-inspired demand forecasting with chronological holdout, weekday effects, MAE and a baseline.

Pronosticar demanda ayuda a planear recursos. Ajusto una tendencia lineal con 84 días y calculo efectos por día de la semana usando solo entrenamiento. Los siguientes 28 días se reservan para prueba. MAE es el promedio del error absoluto. Comparo con repetir la última semana; si no supera ese baseline, el modelo no aporta suficiente valor.

## 2. Git y GitHub desde cero

Git guarda versiones de tu carpeta. GitHub aloja esas versiones para compartirlas. Un repositorio es una carpeta con historial. Un commit es una versión guardada; una branch permite trabajar por separado; un pull request permite revisar el cambio antes de integrarlo. GitHub no se instala: se abre en el navegador. Git sí se instala.

1. Instala Python desde https://www.python.org/downloads/ y Git desde https://git-scm.com/downloads/. En Windows selecciona Add Python to PATH durante la instalación.
2. Abre PowerShell. Escribe `python --version` y `git --version`. Si Python no aparece, prueba `py --version`.
3. Ejecuta `git clone https://github.com/erickvera610/consulting-demand-lab.git`. Clone descarga archivos e historial.
4. Ejecuta `cd consulting-demand-lab`. Ahora estás dentro de la carpeta.
5. Ejecuta `python app.py` (o `py app.py`). La terminal debe mostrar Open http://127.0.0.1:8000.
6. Abre esa dirección en el navegador y usa los controles. No cierres la terminal durante la demostración.
7. Para detenerlo pulsa Ctrl+C. Si el puerto está ocupado, en PowerShell ejecuta `$env:PORT="8001"; python app.py` y abre http://127.0.0.1:8001.

## 3. Cómo se construyó

Primero se definió el problema y un ejemplo pequeño reproducible. Después se escribió el algoritmo en core.py. Se añadieron pruebas para un caso correcto y errores importantes. app.py conecta el algoritmo con una API. index.html permite probarlo sin escribir comandos. Finalmente se añadieron documentación y un workflow de GitHub Actions. Se usó asistencia de IA: tu aprendizaje consiste en comprobar, explicar y modificar lo recibido.

## 4. Leer el código en orden

Abre core.py y busca `run`: recibe el diccionario enviado por el navegador. Lee las funciones llamadas por run y cambia una variable pequeña. Después abre test_core.py: cada test declara una expectativa comprobable. Lee app.py: do_GET entrega la página y do_POST lee JSON y devuelve resultados. Por último lee index.html: api utiliza fetch para enviar datos; los eventos onclick conectan botones con acciones.

## 5. Comprobar que funciona

Detén el servidor y ejecuta `python -m unittest discover -v`. OK indica que pasaron las pruebas, pero no demuestra que no existan otros errores. Reinicia la aplicación y prueba una entrada válida y una inválida. En GitHub abre Actions para revisar el resultado remoto; no confundas pruebas locales con una ejecución de Actions.

## 6. Tu primer cambio real en GitHub

```bash
git switch -c feature/my-first-improvement
```

Edita el texto de un botón o añade una mejora del algoritmo. Ejecuta las pruebas. Después:

```bash
git add .
git commit -m "Improve demonstration and document behavior"
git push -u origin feature/my-first-improvement
```

En GitHub abre Compare & pull request. Describe qué cambiaste, por qué y cómo lo verificaste. Revisa Files changed antes de integrar. La autenticación de Git se hace con el navegador o el gestor de credenciales, no con una contraseña pegada en el código.

## 7. Ejercicios para dominarlo

1. Explica la entrada y salida de run sin leer el README.
2. Añade una prueba para un caso límite diferente.
3. Modifica un parámetro y observa cómo cambia el resultado.
4. Añade una función pequeña y publícala mediante una branch y un pull request.
5. Graba una demostración de dos minutos con el problema, la solución y una limitación.

## 8. Preguntas de entrevista en inglés

- What problem does this project solve?
- How does data move from the browser to Python?
- Why did you separate the core logic from the HTTP handler?
- What edge cases did you test?
- What are the limitations of this prototype?
- What did you personally change after the initial AI-assisted implementation?
- How would you improve this for production?

Respuesta base para practicar: “This is an AI-assisted learning project. I studied the core algorithm, ran the tests, and implemented [your actual change]. The main limitation is [specific limitation].” Sustituye los corchetes por trabajo que realmente hayas realizado.

## Demo pública

Abre https://erickvera610.github.io/consulting-demand-lab/ . Cambia los controles y ejecuta el ejemplo. Python y JavaScript usan generadores distintos; las métricas pueden variar. Los datos son ficticios.
