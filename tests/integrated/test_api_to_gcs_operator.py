from operators.api_to_gcs_operator import ApiToGCSOperator

if __name__ == "__main__":
    op = ApiToGCSOperator(
        task_id="test_api_to_gcs",
        api_url="https://jsonplaceholder.typicode.com/posts",
        gcs_bucket="seu-bucket",
        gcs_path="test/api",
        dag=None  # Fora do DAG
    )
    op.execute(context={})  # Executa localmente
