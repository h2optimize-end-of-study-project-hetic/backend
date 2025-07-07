FROM python:3.12.11-slim-bookworm

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

EXPOSE 80

CMD ["fastapi", "run", "./app/services/http/main.py", "--port", "80", "--reload"]


