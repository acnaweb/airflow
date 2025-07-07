# Projeto 6 - Variáveis, Conexões e Sensores Para Extração e Movimentação de Dados com Airflow

# Imports
from airflow import DAG
from airflow.models import Variable
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.http_sensor import HttpSensor
from airflow.sensors.sql import SqlSensor
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import shutil
import requests
import json
import sqlite3

# Definição de variáveis (devem ser criadas na interface do Airflow)
file_name = Variable.get("file_name")
destination_path = Variable.get("dest_path")
db_path = Variable.get("db_path")
table_name = Variable.get("table_name")
api_key = Variable.get("api_key")

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

# Função para extrair dados da API e salvar em arquivo
def dsa_extrai_dados():
    URL_BASE = "https://api.openweathermap.org/data/2.5/weather?"
    API_KEY = api_key
    CIDADE = "Recife"

    # Construção da URL completa para a requisição
    url = f"{URL_BASE}q={CIDADE}&appid={API_KEY}"

    # Realiza a requisição e retorna a resposta em formato JSON
    response = requests.get(url).json()

    # Caminho completo do arquivo para salvar os dados
    file_path = f"/opt/airflow/dags/fonte/{file_name}"

    # Salva os dados da API no arquivo em formato JSON
    with open(file_path, 'w') as f:
        json.dump(response, f)

    print(f"Dados da API salvos em {file_path}")

# Função para ler o arquivo e inserir os dados no banco de dados SQLite
def insert_into_db():

    # Caminho completo do arquivo
    file_path = f"/opt/airflow/dags/destino/{file_name}"

    # Ler o conteúdo do arquivo
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Verificar se a tabela existe (se não, cria)
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        weather TEXT,
        temperature REAL,
        humidity INTEGER
    )
    """)

    # Inserir os dados na tabela
    city = data['name']
    weather = data['weather'][0]['description']
    temperature = data['main']['temp']
    humidity = data['main']['humidity']

    cursor.execute(f"""
    INSERT INTO {table_name} (city, weather, temperature, humidity)
    VALUES (?, ?, ?, ?)
    """, (city, weather, temperature, humidity))

    # Commit e fechar a conexão
    conn.commit()
    conn.close()

    print(f"Dados inseridos no banco de dados {db_path} na tabela {table_name}")

with DAG('projeto6v4',
         default_args=default_args,
         description='Projeto 6 - DAG V4',
         schedule_interval='@daily',
         catchup=False) as dag:

    # Dummy start task
    start_task = DummyOperator(
        task_id='start_task'
    )

    # File Sensor
    wait_for_file = FileSensor(
        task_id='wait_for_file',
        filepath=file_name,           # Apenas o nome do arquivo
        fs_conn_id='dsa_filesystem',  # Conexão configurada no Airflow
        timeout=600,
        poke_interval=30,
        mode='poke'
    )

    # HTTP Sensor para verificar a disponibilidade da API
    check_api_availability = HttpSensor(
        task_id='check_api_availability',
        http_conn_id='openweathermap_api',  # Conexão configurada no Airflow
        endpoint=f"data/2.5/weather?q=Recife&appid={api_key}",  # Endpoint da API
        timeout=600,
        poke_interval=30,
        mode='poke'
    )

    # SQL Sensor para verificar a disponibilidade da tabela no banco de dados
    check_table_availability = SqlSensor(
        task_id='check_table_availability',
        conn_id='sqlite_default',  # Conexão configurada para o SQLite no Airflow
        sql=f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';",
        timeout=600,
        poke_interval=30,
        mode='poke'
    )

    # PythonOperator para extrair dados da API e salvar no arquivo
    extract_data_task = PythonOperator(
        task_id='extract_data',
        python_callable=dsa_extrai_dados
    )

    # PythonOperator para copiar o arquivo para o destino
    copy_task = PythonOperator(
        task_id='copy_file',
        python_callable=copy_file,
        op_kwargs={'source_path': f'/opt/airflow/dags/fonte/{file_name}', 'destination_path': destination_path}
    )

    # PythonOperator para inserir os dados no banco de dados SQLite
    insert_data_task = PythonOperator(
        task_id='insert_into_db',
        python_callable=insert_into_db
    )

    # Dummy end task
    end_task = DummyOperator(
        task_id='end_task'
    )

    # Definindo as dependências das tarefas
    start_task >> check_api_availability >> extract_data_task >> wait_for_file >> copy_task >> check_table_availability >> insert_data_task >> end_task





    
