FROM python:3.6.4-slim

RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /app

COPY . .

RUN pip install --default-timeout=100 -r requirements.txt