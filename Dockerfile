FROM apache/airflow:2.4.2-python3.10

USER root

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    git wget unzip curl \
    openssh-client iputils-ping groff nano telnet && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* \    
    && python -m pip install --upgrade pip 


USER airflow
WORKDIR /opt/airflow

COPY requirements.* .
RUN pip install --no-cache-dir apache-airflow==${AIRFLOW_VERSION} -r requirements.txt && \
    pip install --no-cache-dir -r requirements.oci.txt && \
    pip install --no-cache-dir -r requirements.dbt.txt && \
    pip install --no-cache-dir -r requirements.gcp.txt
