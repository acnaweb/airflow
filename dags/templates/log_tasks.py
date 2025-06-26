import logging

from airflow.operators.python import PythonOperator


def log_event(message, level="INFO"):
    def _log():
        getattr(logging, level.lower(), logging.info)(message)

    return PythonOperator(task_id=f"log_{level.lower()}", python_callable=_log)
