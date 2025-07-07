# Cap04 - DAG 3

# Este script cria uma DAG no Apache Airflow que será executada diariamente. 
# O script usa um gerenciador de contexto "with" para definir a DAG, o que ajuda a manter o código mais organizado. 
# A DAG contém uma única tarefa que executa um comando bash para imprimir uma mensagem específica. 

# Imports
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.bash import BashOperator

# Definindo argumentos padrões para a DAG
default_args = {
    'owner': 'Data Science Academy',  # Definindo o proprietário da DAG
}

# Criando uma instância de uma DAG usando o gerenciador de contexto 'with'
with DAG(
    dag_id = 'dsa_03_hello_world',        # Identificador único para a DAG
    description = 'Minha Terceira DAG!',  # Descrição da DAG
    default_args = default_args,          # Aplicando os argumentos padrões definidos anteriormente
    start_date = datetime(2023, 12, 29),  # Definindo a data de início 
    end_date = datetime(2024, 1, 1),      # Definindo a data de fim 
    schedule_interval = '@hourly'         # Configurando a DAG para ser executada por hora
) as dsa_dag:
    
    # Criando uma tarefa dentro do gerenciador de contexto da DAG
    dsa_task = BashOperator(
        task_id = 'tarefa_03',                                               # Identificador único para a tarefa
        bash_command = 'echo Hello World DSA - Criando DAG Usando with!!',   # Comando bash que será executado
    )

# Referenciando a tarefa criada
dsa_task
