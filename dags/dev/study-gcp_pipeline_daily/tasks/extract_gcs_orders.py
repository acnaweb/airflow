# ---
# python_callable: run
# ---

from loguru import logger
from typing import List
from google.cloud import storage
from airflow.providers.google.cloud.hooks.gcs import GCSHook


def run(**kwargs):
    bucket = kwargs["params"]["raw_bucket"]
    prefix = f"raw/api/dados"
    gcp_conn_id = kwargs["params"]["gcp_conn_id"]

    return extract_gcs_orders(bucket, prefix, gcp_conn_id)


def extract_gcs_orders(bucket: str, prefix: str, gcp_conn_id: str = "google_cloud_default", **kwargs):
    hook = GCSHook(gcp_conn_id=gcp_conn_id)
    # lista nomes (strings) com o prefixo
    objects = hook.list(bucket_name=bucket, prefix=prefix)
    uris = [f"gs://{bucket}/{obj}" for obj in objects]
    if not uris:
        raise ValueError(f"Nenhum arquivo em gs://{bucket}/{prefix}")
    return uris