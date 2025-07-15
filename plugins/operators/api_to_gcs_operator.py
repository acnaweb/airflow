import requests
import json
import pandas as pd
import gzip
from typing import Optional
from google.cloud import storage
from datetime import datetime
from operators.base_safe_operator import BaseSafeOperator


class ApiToGCSOperator(BaseSafeOperator):
    """
    Operator que faz uma requisição HTTP GET a uma API e salva o conteúdo em um bucket do GCS.
    Pode salvar como .json ou .parquet, com ou sem compressão gzip.
    """

    def __init__(
        self,
        api_url: str,
        gcs_bucket: str,
        gcs_path: str,
        save_as_parquet: bool = False,
        compression: Optional[str] = None,  # 'gzip' ou None
        gcp_conn_id: str = "google_cloud_default",
        **kwargs
    ):
        self.api_url = api_url
        self.gcs_bucket = gcs_bucket
        self.gcs_path = gcs_path
        self.save_as_parquet = save_as_parquet
        self.compression = compression
        self.gcp_conn_id = gcp_conn_id
        super().__init__(**kwargs)

    def run_safe(self, context):
        self.log.info(f"Fazendo requisição para: {self.api_url}")
        response = requests.get(self.api_url)
        response.raise_for_status()

        data = response.json()
        self.log.debug(data)

        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")

        # Escolher extensão do arquivo com base na compressão e formato
        ext = ".parquet" if self.save_as_parquet else ".json"
        if self.compression == "gzip":
            ext += ".gz"

        filename = f"{self.gcs_path.rstrip('/')}/data_{timestamp}{ext}"
        self.log.info(f"Salvando arquivo em: gs://{self.gcs_bucket}/{filename}")

        client = storage.Client()
        bucket = client.get_bucket(self.gcs_bucket)
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

        self.log.info("Upload para o GCS concluído com sucesso.")
