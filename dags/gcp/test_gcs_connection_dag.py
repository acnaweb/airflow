from airflow.decorators import dag, task
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.utils.dates import days_ago


@dag(
    dag_id="test_gcs_connection",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=["test", "gcp", "gcs"],
)
def gcs_connection_test_dag():
    @task
    def listar_buckets():
        hook = GCSHook(gcp_conn_id="google_cloud_default")
        client = hook.get_conn()  # Retorna um google.cloud.storage.Client
        buckets = list(client.list_buckets())

        print("Buckets disponíveis:")
        for bucket in buckets:
            print(f"✅ {bucket.name}")

    listar_buckets()


gcs_connection_test_dag()
