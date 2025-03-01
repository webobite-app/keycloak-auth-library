# Development
FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install -e .

CMD ["flask", "run", "--host=0.0.0.0"]

# Production
FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -e . gunicorn

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app:app"]