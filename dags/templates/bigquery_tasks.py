from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyTableOperator, BigQueryInsertJobOperator)


def run_bq_query(query, location="US"):
    return BigQueryInsertJobOperator(
        task_id="run_bq_query",
        configuration={"query": {"query": query, "useLegacySql": False}},
        location=location,
    )


def create_empty_table(project, dataset, table, schema_fields):
    return BigQueryCreateEmptyTableOperator(
        task_id=f"create_table_{table}",
        project_id=project,
        dataset_id=dataset,
        table_id=table,
        schema_fields=schema_fields,
    )
