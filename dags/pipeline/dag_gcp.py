import os

from templates.gcs_tasks import create_bucket, download_file_from_gcs

from airflow.decorators import dag
from airflow.models.variable import Variable

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

    downloaded = download_file_from_gcs(
        "bucket-name", "data/filename.csv", "/tmp/arquivo.csv"
    )

    created_bucket = create_bucket("bucket-playground", GOOGLE_CLOUD_PROJECT)

    (downloaded >> created_bucket)


dag_gcp()
