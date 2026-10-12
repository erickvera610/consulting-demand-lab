FROM python:3.12-slim
WORKDIR /app
COPY requirements-model.txt .
RUN pip install --no-cache-dir -r requirements-model.txt
COPY . .
RUN useradd --create-home appuser
USER appuser
ENV HOST=0.0.0.0 PORT=8001
EXPOSE 8001
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8001/health', timeout=2).read()" || exit 1
CMD ["python", "model_server.py"]
