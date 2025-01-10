# Cap04 - DAG 1

# DAG é a sigla para Directed Acyclic Graph (Grafo Acíclico Dirigido).
# Uma DAG é um conjunto de tarefas e suas dependências. No Airflow, cada nó do grafo representa uma tarefa e as arestas 
# representam as dependências entre estas tarefas.

# Este script define uma DAG no Apache Airflow com uma única tarefa que executa um comando bash para imprimir "Hello world!". 

# Importando datetime e timedelta do módulo datetime
from datetime import datetime, timedelta

# Importando days_ago da biblioteca airflow.utils.dates
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
    dag_id = 'dsa_01_hello_world',               # Identificador único para a DAG
    description = 'Minha Primeira DAG!',         # Descrição da DAG
    default_args = default_args,                 # Aplicando os argumentos padrões definidos anteriormente
    start_date = days_ago(1),                    # Definindo a data de início como um dia atrás
    schedule_interval = None                     # Configurando a DAG para não ter um intervalo de agendamento
)

# Criando uma tarefa usando BashOperator
dsa_task = BashOperator(
    task_id = 'tarefa_01',                        # Identificador único para a tarefa
    bash_command = 'echo Hello World DSA!',       # Comando bash que será executado
    dag = dsa_dag                                 # Associando a tarefa à DAG criada anteriormente
)

# Referenciando a tarefa criada
dsa_task
