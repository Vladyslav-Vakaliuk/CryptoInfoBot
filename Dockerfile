# syntax=docker/dockerfile:1

FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./bot /code/bot

CMD ["python", "bot/main.py"]