FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY metrics_exporter.py .
USER 65534:65534
EXPOSE 8008
CMD ["python", "metrics_exporter.py"]
