FROM apache/airflow:2.4.3
USER root
RUN apt update && apt -y install git
USER airflow
ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt

