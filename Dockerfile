# syntax=docker/dockerfile:1

FROM python:3.11.1-slim-buster

WORKDIR /bot

COPY requirements.txt /bot/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /bot/requirements.txt

COPY ./ /bot/

CMD ["python", "bot.py"]