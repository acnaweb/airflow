# Projeto 6 - Variáveis, Conexões e Sensores Para Extração e Movimentação de Dados com Airflow

# Imports
from airflow import DAG
from airflow.models import Variable
from airflow.sensors.filesystem import FileSensor
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import shutil

# Definição de variáveis (devem ser criadas na interface do Airflow)
file_name = Variable.get("file_name")
destination_path = Variable.get("dest_path")

# Argumentos
default_args = {
    "owner": "Data Science Academy",
    'start_date': datetime(2024, 10, 18),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Função para copiar o arquivo
def copy_file(source_path, destination_path):
    shutil.copy(source_path, destination_path)
    print(f"Arquivo copiado de {source_path} para {destination_path}")

with DAG('projeto6v1',
         default_args=default_args,
         description='Projeto 6 - DAG V1',
         schedule_interval='@daily',
         catchup=False) as dag:

    # Dummy start task
    start_task = DummyOperator(
        task_id='start_task'
    )

    # File Sensor
    wait_for_file = FileSensor(task_id='wait_for_file',
                               filepath=file_name,           # Apenas o nome do arquivo
                               fs_conn_id='dsa_filesystem',  # Conexão configurada no Airflow
                               timeout=600,                  # Timeout de 10 minutos
                               poke_interval=5,              # Intervalo de 5 segundos para testes rápidos
                               mode='poke')

    # PythonOperator para copiar o arquivo
    copy_task = PythonOperator(
        task_id='copy_file',
        python_callable=copy_file,
        op_kwargs={'source_path': f'/opt/airflow/dags/fonte/{file_name}', 'destination_path': destination_path}
    )

    # Dummy end task
    end_task = DummyOperator(
        task_id='end_task'
    )

    # Definindo as dependências das tarefas
    start_task >> wait_for_file >> copy_task >> end_task





    
