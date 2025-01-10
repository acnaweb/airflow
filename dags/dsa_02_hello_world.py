# Cap04 - DAG 2

# Este script cria uma DAG no Apache Airflow que é programada para ser executada diariamente. 
# A DAG contém uma única tarefa que executa um comando bash para imprimir "Hello World!"

# Importando as funções datetime e timedelta do módulo datetime
from datetime import datetime, timedelta

# Importando a função days_ago da biblioteca airflow.utils.dates
from airflow.utils.dates import days_ago

# Importando DAG da biblioteca airflow
from airflow import DAG

# Importando BashOperator da biblioteca airflow.operators.bash
from airflow.operators.bash import BashOperator

# Definindo argumentos padrões para a DAG
default_args = {
    'owner': 'Data Science Academy',  # Definindo o proprietário da DAG
}

# Criando uma instância de uma DAG
dsa_dag = DAG(
    dag_id = 'dsa_02_hello_world',         # Identificador único para a DAG
    description = 'Minha Segunda DAG!',    # Descrição da DAG
    default_args = default_args,           # Aplicando os argumentos padrões definidos anteriormente
    start_date = days_ago(1),              # Definindo a data de início como um dia atrás
    schedule_interval = '@daily',          # Configurando a DAG para ser executada diariamente
    tags = ['dsa', 'bash', 'hello world']  # Tags para facilitar a organização e a busca da DAG
)

# Criando uma tarefa usando BashOperator
dsa_task = BashOperator(
    task_id = 'tarefa_02',                           # Identificador único para a tarefa
    bash_command = 'echo Hello World DSA!',          # Comando bash que será executado
    dag = dsa_dag                                    # Associando a tarefa à DAG criada anteriormente
)

# Referenciando a tarefa criada
dsa_task
