# ---
# dependencies:
#   - extract_gcs_orders
# python_callable: run
# ---

from loguru import logger
from typing import List
from google.cloud import storage
from airflow.providers.google.cloud.hooks.gcs import GCSHook


def run(**kwargs):
    ti = kwargs["ti"]
    input_files = ti.xcom_pull(task_ids='extract_gcs_orders', key='return_value')
    return transform_orders_clean(input_files)


def transform_orders_clean(input_files: List[str], **kwargs):
    """
    Exemplo didático:
    - para dados pequenos: retornar lista de dicts (usado pela opção UNNEST).
    - para volume alto: gerar NDJSON em 'staging/orders_clean/<data>/*.json' e retornar esse path.
    """

    logger.info(input_files)
    # TODO: ler arquivos 'input_files', normalizar e retornar 'records' OU caminho no GCS.
    records = [
        {"order_id": "A123", "created_at": "2025-08-18T03:00:00Z", "amount": "100.50", "customer_id": "C001"},
        {"order_id": "B456", "created_at": "2025-08-18T03:10:00Z", "amount": "59.90", "customer_id": "C002"},
    ]
    return records