FROM apache/airflow:slim-2.9.3-python3.10

ENV AIRFLOW_UID=1000

USER airflow
WORKDIR /opt/airflow

COPY requirements.* .
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir apache-airflow==${AIRFLOW_VERSION} -r requirements.txt
