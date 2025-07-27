FROM python:3.13-slim AS base

WORKDIR /app

# Встановлюємо Poetry
RUN pip install --no-cache-dir poetry

# Копіюємо тільки файли для залежностей (кеш)
COPY pyproject.toml poetry.lock ./

# Встановлюємо продакшн-залежності
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev

# Копіюємо код додатку
COPY . .

# Аргумент для визначення режиму запуску
ARG TARGET=api

ARG WORKER_FILE=run_export_worker.py
ARG API_FILE=run.py

# Запуск: API (uvicorn) або Worker
CMD ["sh", "-c", "if [ \"$TARGET\" = 'worker' ]; then poetry run python $WORKER_FILE; else poetry run python $API_FILE; fi"]
