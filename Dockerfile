FROM python:3.11-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt 

COPY ./app /code/app

RUN adduser --disabled-password --no-create-home appuser



# Development
FROM base AS development

RUN chmod +x /code/app/src/init_db.sh

EXPOSE 80

CMD ["/code/app/src/init_db.sh", "uvicorn", "app.src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]



# Production
FROM base AS production

RUN chmod +x /code/app/src/init_db.sh

EXPOSE 80

USER appuser

CMD ["/code/app/src/init_db.sh", "gunicorn", "app.src.main:app", "-c", "/code/app/src/gunicorn.conf.py"]
