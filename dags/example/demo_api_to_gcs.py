from datetime import datetime

from operators.api_to_gcs_operator import ApiToGCSOperator

from airflow.decorators import dag


@dag(
    dag_id="demo_api_to_gcs",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["demo", "api", "gcs"],
    description=(
        "Extrai dados de uma API pública e salva no GCS"
        " como JSON usando operador customizado."
    ),
)
def api_to_gcs_pipeline():
    export_api_data = ApiToGCSOperator(
        task_id="json_sem_gzip",
        api_url="https://randomuser.me/api/",
        gcs_bucket="acnaweb-bucket-general",
        gcs_path="raw/api/dados",
    )

    export_api_data  # registra no DAG


api_to_gcs_pipeline()
