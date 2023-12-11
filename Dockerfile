FROM python:3.8

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /app/backend
WORKDIR /app/backend
COPY . /app/backend
RUN apt-get update && apt-get install -y postgresql-client
RUN pip install --upgrade pip
RUN pip install -r requirements.txt