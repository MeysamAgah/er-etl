FROM apache/airflow:latest

USER root

RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

USER airflow

COPY ../requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt