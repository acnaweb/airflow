# operators/api_to_gcs_operator.py

import requests
import json
from airflow.utils.decorators import apply_defaults
from google.cloud import storage
from datetime import datetime
from operators.base_safe_operator import BaseSafeOperator



class ApiToGCSOperator(BaseSafeOperator):
    """
    Operator que faz uma requisição HTTP GET a uma API e salva o conteúdo em um bucket do GCS.
    """

    def __init__(self, api_url, gcs_bucket, gcs_path, gcp_conn_id='google_cloud_default', **kwargs):
        super().__init__(**kwargs)
        self.api_url = api_url
        self.gcs_bucket = gcs_bucket
        self.gcs_path = gcs_path
        self.gcp_conn_id = gcp_conn_id


    def run_safe(self, context):
        self.log.info(f"Fazendo requisição para: {self.api_url}")
        response = requests.get(self.api_url)
        response.raise_for_status()

        data = response.json()

        self.log.debug(data)

        # Opcional: timestamp no arquivo
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        filename = f"{self.gcs_path.rstrip('/')}/data_{timestamp}.json"

        self.log.info(f"Salvando arquivo em: gs://{self.gcs_bucket}/{filename}")

        client = storage.Client()
        bucket = client.get_bucket(self.gcs_bucket)
        blob = bucket.blob(filename)
        blob.upload_from_string(json.dumps(data), content_type="application/json")

        self.log.info("Upload para o GCS concluído com sucesso.")



