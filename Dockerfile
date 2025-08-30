FROM python:3.11-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc libpq-dev curl build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY /app/pyproject.toml /code/
RUN pip install .



FROM base AS development

RUN pip install -e ".[dev]"

COPY ./app /code/app

EXPOSE 80

CMD ["/code/app/init_db.sh", "uvicorn", "app.src.presentation.main:app", "--host", "0.0.0.0", "--port", "80", "--reload", "--reload-dir", "/code/app/src"]


FROM base AS production

RUN adduser --disabled-password --no-create-home appuser

COPY --chown=appuser:appuser ./app /code/app

USER appuser

EXPOSE 80

CMD ["/code/app/init_db.sh", "gunicorn", "app.src.presentation.main:app", "-c", "/code/app/gunicorn.conf.py"]