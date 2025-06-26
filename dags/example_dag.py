# from templates.bigquery_tasks import run_bq_query
# from templates.gcs_tasks import download_file_from_gcs

# from airflow import DAG
# from airflow.utils.dates import days_ago

# with DAG("dag_exemplo_reuso", start_date=days_ago(1), schedule_interval=None) as dag:
#     download = download_file_from_gcs(
#         "meu-bucket", "dados/arquivo.csv", "/tmp/arquivo.csv"
#     )
#     bq = run_bq_query("SELECT COUNT(*) FROM `meuprojeto.dataset.tabela`")

#     download >> bq
