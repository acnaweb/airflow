from airflow.providers.google.cloud.operators.gcs import GCSCreateBucketOperator
from airflow.providers.google.cloud.transfers.gcs_to_local import GCSToLocalFilesystemOperator


def create_bucket(bucket_name, project_id):
    return GCSCreateBucketOperator(
        task_id=f"create_bucket_{bucket_name}",
        bucket_name=bucket_name,
        project_id=project_id,
    )


def download_file_from_gcs(bucket, object_name, local_path):
    return GCSToLocalFilesystemOperator(
                            task_id=f"download_{object_name.replace('/', '_')}",
                            bucket=bucket,
                            object_name=object_name,
                            filename=local_path,
                             )
