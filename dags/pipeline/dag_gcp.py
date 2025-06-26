import os
from airflow.decorators import dag
from airflow.models.variable import Variable
from templates.gcs_tasks import download_file_from_gcs


# Configurações do GCP
GOOGLE_CLOUD_REGION = Variable.get("GOOGLE_CLOUD_REGION")
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", None)

if GOOGLE_CLOUD_PROJECT is None:
    GOOGLE_CLOUD_PROJECT = Variable.get("GOOGLE_CLOUD_PROJECT")


# Definição padrão para o DAG
default_args = {
    "owner": "acnaweb",
    "retries": 0,
}


@dag(
    default_args=default_args,
    schedule_interval=None,
    start_date=None,
    catchup=False,
    tags=["jobs", "monitoramento", "tag"],
)
def dag_gcp():
    download = download_file_from_gcs(
        "abc-composer-dags-prd", "data/dsa-p1-entrada.txt", "/tmp/arquivo.csv"
    )

    download

dag_gcp()
