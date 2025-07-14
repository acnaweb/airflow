# dags/example_api_to_gcs_dag.py

from datetime import datetime

from operators.api_to_gcs_operator import ApiToGCSOperator

from airflow import DAG

with DAG(
    dag_id="api_to_gcs_dag",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["example", "api", "gcs"],
) as dag:

    export_api_data = ApiToGCSOperator(
        task_id="fetch_and_upload_data",
        api_url="https://jsonplaceholder.typicode.com/posts",
        gcs_bucket="meu-bucket-datalake",
        gcs_path="raw/api/posts",
    )
