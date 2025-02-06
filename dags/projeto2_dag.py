# Projeto 2 - Extração de Dados via API com Apache Airflow

# Imports
import datetime as dt
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.utils.dates import days_ago
from projeto2_etl import dsa_processo_etl

# Argumentos
default_args ={
    'owner':'Data Science Academy',
    'depends_on_past':False,
    'start_date':dt.datetime.today(),
    'email':['suporte@datascienceacademy.com.br'],
    'email_on_failure':False,
    'email_on_retry':False,
    'retries':1,
    'retry_delay':timedelta(minutes=1)
}

# DAG
dsa_dag = DAG('projeto2_dag',
              default_args = default_args,
              description = 'Projeto 2',
              schedule_interval = timedelta(minutes=60)
)

# PythonOperator
executa_etl = PythonOperator(task_id = 'projeto2_etl_api',
                             python_callable = dsa_processo_etl,
                             dag = dsa_dag
)

# Envia a tarefa para execução
executa_etl


