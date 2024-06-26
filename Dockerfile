FROM apache/airflow:2.4.2-python3.10
USER root
RUN apt update && apt -y install git libaio1 wget unzip && python -m pip install --upgrade pip

ADD server/install_oracle_client.sh .
RUN bash install_oracle_client.sh

USER airflow
WORKDIR /opt/airflow

COPY requirements.* .
RUN pip install --no-cache-dir apache-airflow==${AIRFLOW_VERSION} -r requirements.txt && \
    pip install --no-cache-dir -r requirements.oci.txt && \
    pip install --no-cache-dir -r requirements.dbt.txt && \
    pip install --no-cache-dir -r requirements.gcp.txt

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/oracle/instantclient
ENV TNS_ADMIN=/opt/oracle/instantclient/network/admin
