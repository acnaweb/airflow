import os
import requests
import json
import pandas as pd
import gzip
from typing import Optional
from datetime import datetime, timezone
from operators.base_safe_operator import BaseSafeOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from google.cloud import storage

class ApiToGCSOperator(BaseSafeOperator):
    """
    Operator que faz uma requisição HTTP GET a uma API e salva o conteúdo em um bucket do GCS.
    Pode salvar como .json ou .parquet, com ou sem compressão gzip.

    A autenticação segue esta ordem:
    1. GOOGLE_APPLICATION_CREDENTIALS
    2. Airflow Connection via gcp_conn_id
    """

    def __init__(
            self,
            api_url: str,
            gcs_bucket: str,
            gcs_path: str,
            save_as_parquet: bool = False,
            compression: Optional[str] = None,
            gcp_conn_id: Optional[str] = "google_cloud_default",
            alert_email: Optional[str] = None,
            **kwargs
        ):        
        super().__init__(**kwargs)
        self.gcp_conn_id = gcp_conn_id
        self.alert_email = alert_email

        self.api_url = api_url
        self.gcs_bucket = gcs_bucket
        self.gcs_path = gcs_path
        self.save_as_parquet = save_as_parquet
        self.compression = compression
                                      

    def run_safe(self, context):
        self.log.info(f"Fazendo requisição para: {self.api_url}")
        response = requests.get(self.api_url)
        response.raise_for_status()

        data = response.json()
        self.log.debug(f"Dados recebidos: {str(data)[:500]}")

        
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")


        ext = ".parquet" if self.save_as_parquet else ".json"
        if self.compression == "gzip":
            ext += ".gz"

        filename = f"{self.gcs_path.rstrip('/')}/data_{timestamp}{ext}"
        self.log.info(f"Salvando arquivo em: gs://{self.gcs_bucket}/{filename}")

        # ✅ Agora usando método da superclasse
        client = self.get_gcp_storage_client()
        bucket = client.bucket(self.gcs_bucket)
        blob = bucket.blob(filename)

        if self.save_as_parquet:
            df = pd.DataFrame(data if isinstance(data, list) else [data])
            parquet_bytes = df.to_parquet(index=False, compression=self.compression or "snappy")
            blob.upload_from_string(parquet_bytes, content_type="application/octet-stream")
        else:
            json_data = json.dumps(data).encode("utf-8")
            if self.compression == "gzip":
                json_data = gzip.compress(json_data)
                content_type = "application/gzip"
            else:
                content_type = "application/json"
            blob.upload_from_string(json_data, content_type=content_type)

        self.log.info("✅ Upload para o GCS concluído com sucesso.")

    def get_gcp_storage_client(self):
        """
        Retorna um client autenticado do Google Cloud Storage.

        Prioridade:
        1. GOOGLE_APPLICATION_CREDENTIALS (variável de ambiente)
        2. gcp_conn_id (conexão configurada na UI do Airflow)
        """
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            self.log.info("🔐 Autenticando com GOOGLE_APPLICATION_CREDENTIALS.")
            return storage.Client()
        else:
            self.log.info(f"🔐 Autenticando via gcp_conn_id='{self.gcp_conn_id}'.")
            hook = GCSHook(gcp_conn_id=self.gcp_conn_id)
            return hook.get_conn()
        
        