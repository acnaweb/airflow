import os

from templates.gcs_tasks import create_bucket, download_file_from_gcs
from templates.bigquery_tasks import create_empty_table
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

    schema_fields = [
            {"name": "id", "type": "STRING", "mode": "REQUIRED"},
            {"name": "nome", "type": "STRING", "mode": "NULLABLE"},
            {"name": "idade", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "criado_em", "type": "TIMESTAMP", "mode": "REQUIRED"},
            {
                "name": "endereco",
                "type": "RECORD",
                "mode": "NULLABLE",
                "fields": [
                    {"name": "rua", "type": "STRING", "mode": "NULLABLE"},
                    {"name": "numero", "type": "INTEGER", "mode": "NULLABLE"},
                ],
            },
        ]


    created_table = create_empty_table("abc-sbx-engenhariadados", "DS_AC", "tb_demo", schema_fields)

    downloaded >> created_bucket >> created_table


dag_gcp()
