from datetime import datetime

from operators.api_to_bq_operator import ApiToBigqueryOperator

from airflow.decorators import dag
from airflow.providers.google.cloud.operators.bigquery import \
    BigQueryInsertJobOperator


@dag(
    dag_id="demo_api_to_bq",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["demo", "api", "bigquery"],
    description=(
        "Extrai dados de uma API pública e salva no BigQuery "
        "usando schema padronizado de ingestão."
    ),
)
def demo_api_to_bq():
    export_api_data = ApiToBigqueryOperator(
        task_id="exportar_dados_api",
        api_url="https://randomuser.me/api/?results=5",
        project_id="study-gcp-398200",  # ⬅️ substitua pelo ID do seu projeto
        dataset_id="raw",  # ⬅️ substitua se necessário
        table_id="stg_random_users",  # ⬅️ substitua se necessário
        gcp_conn_id="google_cloud_default",  # ou configure GOOGLE_APPLICATION_CREDENTIALS
    )

    call_procedure = BigQueryInsertJobOperator(
        task_id="call_transform_procedure",
        configuration={
            "query": {
                "query": "CALL `study-gcp-398200.raw.transform_to_bronze`()",
                "useLegacySql": False,
            }
        },
        location="us-west1",  # ou "southamerica-east1" se aplicável
        gcp_conn_id="google_cloud_default",  # ou defina outra conexão
    )

    export_api_data >> call_procedure


demo_api_to_bq()
