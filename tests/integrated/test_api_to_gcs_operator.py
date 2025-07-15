from operators.api_to_gcs_operator import ApiToGCSOperator

if __name__ == "__main__":
    try:
        
        op = ApiToGCSOperator(
            task_id="json_sem_gzip",
            api_url="https://randomuser.me/api/",
            gcs_bucket="acnaweb-bucket-general",
            gcs_path="raw/api/dados",
        )

        op.execute(context={})  # Executa localmente
    except Exception as e:
        pass

    op = ApiToGCSOperator(
        task_id="json_com_gzip",
        api_url="https://randomuser.me/api/",
        gcs_bucket="acnaweb-bucket-general",
        gcs_path="raw/api/dados",
        compression="gzip"
    )

    op.execute(context={})  # Executa localmente    

    op = ApiToGCSOperator(
        task_id="parquet_com_gzip",
        api_url="https://randomuser.me/api/",
        gcs_bucket="acnaweb-bucket-general",
        gcs_path="raw/api/dados",
        save_as_parquet=True,
        compression="gzip"
    )
    
    op.execute(context={})  # Executa localmente        
