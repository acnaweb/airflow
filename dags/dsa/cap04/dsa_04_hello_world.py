# Cap04 - DAG 4

# Este script cria uma DAG no Apache Airflow com duas tarefas que são executadas uma vez. 
# A tarefa B é configurada para depender da tarefa A, o que significa que a tarefa B só será 
# executada após a conclusão bem-sucedida da tarefa A.

# Imports
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.bash import BashOperator

# Definindo argumentos padrões para a DAG
default_args = {
    'owner': 'Data Science Academy',                 # Definindo o proprietário da DAG
    'email': ['suporte@datascienceacademy.com.br'],  # E-mails para notificação
    'email_on_failure': False,                       # Desativando o envio de e-mail em caso de falha
    'email_on_retry': False,                         # Desativando o envio de e-mail em caso de nova tentativa
    'retries': 1,                                    # Definindo o número de tentativas em caso de falha
    'retry_delay': timedelta(minutes=5),             # Definindo o intervalo de tempo entre as tentativas
}

# Define uma data futura para start_date
future_date = datetime(2024, 2, 1)  # Ano, Mês, Dia

# Criando uma instância de uma DAG usando o gerenciador de contexto 'with'
with DAG(
    dag_id = 'dsa_04_hello_world',                       # Identificador único para a DAG
    description = 'DAG com mais de uma tarefa',          # Descrição da DAG
    default_args = default_args,                         # Aplicando os argumentos padrões definidos anteriormente
    start_date = future_date,                            # Definindo a data de início como uma data futura
    schedule_interval = '@once'                          # Configurando a DAG para ser executada apenas uma vez
) as dsa_dag:

    # Criando a primeira tarefa usando BashOperator
    dsaTarefaA = BashOperator(
        task_id = 'dsaTarefaA',                                         # Identificador único para a tarefa A
        bash_command = 'echo Tarefa A Executada com Sucesso DSA!'       # Comando bash que será executado pela tarefa A
    )

    # Criando a segunda tarefa usando BashOperator
    dsaTarefaB = BashOperator(
        task_id = 'dsaTarefaB',                                         # Identificador único para a tarefa B
        bash_command = 'echo Tarefa B Executada com Sucesso DSA!'       # Comando bash que será executado pela tarefa B
    )

# Definindo a dependência entre as tarefas: dsaTarefaB depende de dsaTarefaA
dsaTarefaB.set_upstream(dsaTarefaA)







