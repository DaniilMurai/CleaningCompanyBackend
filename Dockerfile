FROM python:3.13-slim AS base

WORKDIR /app

# Installing Poetry
RUN pip install --no-cache-dir poetry

# Copying dependency files (cache)
COPY pyproject.toml poetry.lock ./

# Installing system dependencies
RUN apt-get update && apt-get install -y build-essential gcc libffi-dev tzdata && rm -rf /var/lib/apt/lists/*

# Disabling creating virtual env & Installing prod dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction

# Copying an app code
COPY . .

# Default starting argument
ARG TARGET=api
ENV TARGET=$TARGET

ARG WORKER_FILE=run_export_worker.py
ARG API_FILE=run.py

# Running api or worker
CMD ["sh", "-c", "if [ \"$TARGET\" = 'worker' ]; then echo \"running worker\" && poetry run python $WORKER_FILE; else echo \"running API\" && poetry run python $API_FILE; fi"]
