# Guia de Padrões para Nome de *Tasks* (Airflow/Gusty)

Este guia define um vocabulário comum e regras para **`task_id`** em DAGs Airflow (incluindo YAML do Gusty).

---

## ✅ Regras de Nomeação (`task_id`)
- Formato: **`<acao>_<objeto>[_<detalhe>]`**
- Estilo: `snake_case` (minúsculas, sem acentos/espacos)
- Curto e específico (ideal ≤ 50 chars)
- Estável (evite renomear em produção)
- Diferencie tarefas paralelas com sufixos claros (`_sales`, `_customers`, `_step1`)

---

## 📖 Vocabulário de Prefixos (Ações Padrão)

| Prefixo | Significado | Exemplos recomendados |
|---|---|---|
| **extract** | Extrair dados de uma fonte | `extract_gcs_orders`, `extract_api_customers`, `extract_mysql_transactions` |
| **load** | Carregar dados em destino | `load_bq_orders`, `load_gcs_raw`, `load_postgres_dim_products` |
| **transform** | Processar/limpar/normalizar | `transform_orders_clean`, `transform_customers_normalize` |
| **validate** | Validar integridade/qualidade | `validate_schema_orders`, `validate_rowcount_orders` |
| **check** | Checagens simples/guards | `check_bq_rowcount`, `check_null_values` |
| **aggregate** | Agregar/sumarizar | `aggregate_sales_daily`, `aggregate_events_hourly` |
| **export** | Exportar para sistema externo | `export_to_gcs`, `export_to_csv`, `export_to_api` |
| **import** | Importar de arquivos/planilhas | `import_csv_customers`, `import_google_sheets` |
| **notify** | Alertas e notificações | `notify_slack_failure`, `notify_email_success` |
| **trigger** | Disparar outro job/DAG/serviço | `trigger_downstream_dag`, `trigger_cloud_function` |
| **cleanup** | Limpeza de temporários/staging | `cleanup_tmp_gcs`, `cleanup_bq_staging` |
| **archive** | Arquivamento/camada fria | `archive_orders_2024`, `archive_logs_daily` |
| **backup** | Cópias de segurança | `backup_bq_dataset`, `backup_gcs_bucket` |
| **restore** | Restauração de backups | `restore_bq_snapshot` |
| **sync** | Sincronização entre sistemas | `sync_users_crm_to_bq` |
| **split** | Dividir/particionar dados | `split_large_file`, `partition_events_daily` |
| **merge** | Unir/join de coleções | `merge_customer_profiles` |
| **publish** | Publicar dados prontos (bus/evento) | `publish_orders_pubsub`, `publish_kafka_topic` |

> **Dica:** escolha **um** prefixo por tarefa; evite combinações como `extract_load_*`. Separe em duas tasks.

---

## 🧩 Exemplos de Boas Nomes
- `extract_gcs_orders`  
- `transform_orders_clean`  
- `validate_schema_orders`  
- `load_bq_orders`  
- `notify_slack_failure`

## 🚫 Evite
- `task1`, `final`, `run`, `default` (genéricos/ambíguos)  
- `extract` (sozinho)  
- Maiúsculas, espaços, acentos

---

## 🔗 Padrão em YAML (Gusty)
```yaml
operator: airflow.providers.google.cloud.transfers.gcs_to_bigquery.GCSToBigQueryOperator
args:
  task_id: load_bq_orders
  bucket: "{{ params.raw_bucket }}"
  source_objects: ["orders/{{ ds }}/orders-*.json"]
  destination_project_dataset_table: "{{ params.project_id }}:{{ params.dataset }}.orders"
  write_disposition: "WRITE_APPEND"
  location: "{{ params.location }}"
```

---

## ✅ Checklist Rápido
- [ ] `task_id` começa com verbo da tabela de prefixos
- [ ] É específico quanto ao objeto (ex.: `*_orders`, `*_customers`)
- [ ] snake_case e curto
- [ ] Não contém PII ou segredos
- [ ] Mantém consistência com tasks irmãs (mesmo vocabulário)