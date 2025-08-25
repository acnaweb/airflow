import os
import json
import requests
from datetime import datetime, timezone
from typing import Optional
from google.cloud import bigquery
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from operators.base_safe_operator import BaseSafeOperator


class ApiToBigqueryOperator(BaseSafeOperator):
    """
    Operator que faz uma requisição HTTP GET e insere dados em uma tabela padrão de ingestão no BigQuery.
    Cria a tabela automaticamente se ela não existir.
    """

    def __init__(
        self,
        api_url: str,
        project_id: str,
        dataset_id: str,
        table_id: str,
        gcp_conn_id: Optional[str] = "google_cloud_default",
        alert_email: Optional[str] = None,
        write_disposition: str = "WRITE_APPEND",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.api_url = api_url
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.gcp_conn_id = gcp_conn_id
        self.alert_email = alert_email
        self.write_disposition = write_disposition

    def run_safe(self, context):
        self.log.info(f"📥 Requisição para API: {self.api_url}")
        response = requests.get(self.api_url)
        response.raise_for_status()
        data = response.json()

        raw_json = json.dumps(data)
        now = datetime.now(timezone.utc)
        record_count = len(data) if isinstance(data, list) else 1

        row = {
            "raw_data": raw_json,
            "extraction_time": now.isoformat(),
            "source_url": self.api_url,
            "record_count": record_count
        }

        client = self.get_bigquery_client()
        table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"

        self.ensure_table_exists(client, self.project_id, self.dataset_id, self.table_id)

        self.log.info(f"📤 Inserindo dados na tabela {table_ref}")
        errors = client.insert_rows_json(table_ref, [row])
        if errors:
            raise Exception(f"❌ Erro ao inserir dados no BigQuery: {errors}")
        
        self.log.info(f"✅ Dados inseridos com sucesso em {table_ref}")

    def get_bigquery_client(self):
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            self.log.info("🔐 Autenticando com GOOGLE_APPLICATION_CREDENTIALS.")
            return bigquery.Client(project=self.project_id)
        else:
            self.log.info(f"🔐 Autenticando via gcp_conn_id='{self.gcp_conn_id}'.")
            hook = BigQueryHook(gcp_conn_id=self.gcp_conn_id, use_legacy_sql=False)
            return hook.get_client(project_id=self.project_id)

    def ensure_table_exists(self, client, project_id, dataset_id, table_id):
        table_ref = bigquery.TableReference(
            bigquery.DatasetReference(project_id, dataset_id),
            table_id
        )

        try:
            client.get_table(table_ref)
            self.log.info(f"✅ Tabela {project_id}.{dataset_id}.{table_id} já existe.")
        except Exception:
            self.log.warning(f"⚠️ Tabela {project_id}.{dataset_id}.{table_id} não existe. Criando...")
            schema = [
                bigquery.SchemaField("raw_data", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("extraction_time", "TIMESTAMP", mode="REQUIRED"),
                bigquery.SchemaField("source_url", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("record_count", "INTEGER", mode="REQUIRED"),
            ]
            table = bigquery.Table(table_ref, schema=schema)
            table.time_partitioning = bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field="extraction_time"
            )
            client.create_table(table)
            self.log.info(f"✅ Tabela criada: {project_id}.{dataset_id}.{table_id}")
