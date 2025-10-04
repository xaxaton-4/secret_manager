FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY . /app
RUN mkdir /app/log
RUN echo "" > /app/log/secret_manager.log
