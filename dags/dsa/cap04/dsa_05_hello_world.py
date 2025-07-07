# Cap04 - DAG 5

# Dependências entre as DAGs

# Imports
import datetime as dt
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

# Criando uma instância de uma DAG usando o gerenciador de contexto 'with'
with DAG(
    dag_id = 'dsa_05_hello_world',                             # Identificador único para a DAG
    description = 'DAG com múltiplas tarefas e dependências',  # Descrição da DAG
    default_args = default_args,                               # Aplicando os argumentos padrões definidos anteriormente
    start_date = dt.datetime.today(),                          # Data de início
    schedule_interval = timedelta(days=1),                     # Configurando a DAG para ser executada diariamente
    tags = ['dsa', 'dependencias']                             # Tags para facilitar a organização e busca da DAG
) as dsa_dag:

    # Criando a primeira tarefa (dsaTarefaA) usando BashOperator
    dsaTarefaA = BashOperator(
        task_id = 'dsaTarefaA',
        bash_command = '''
            echo Tarefa A Começou!
            
            for i in {1..10}
            do
                echo Tarefa A imprimindo $i
            done

            echo Tarefa A Concluída com Sucesso DSA!
        '''
    )

    # Criando a segunda tarefa (dsaTarefaB) usando BashOperator
    dsaTarefaB = BashOperator(
        task_id = 'dsaTarefaB',
        bash_command = '''
            echo Tarefa B Começou!
            sleep 4
            echo Tarefa B Finalizou!
        '''
    )

    # Criando a terceira tarefa (dsaTarefaC) usando BashOperator
    dsaTarefaC = BashOperator(
        task_id = 'dsaTarefaC',
        bash_command = '''
            echo Tarefa C Começou!
            sleep 15
            echo Tarefa C Finalizou!
        '''
    )
    
    # Criando a quarta tarefa (dsaTarefaD) usando BashOperator
    dsaTarefaD = BashOperator(
        task_id = 'dsaTarefaD',
        bash_command = 'echo Tarefa D Executada com Sucesso DSA!'
    )

# Definindo as dependências das tarefas:
# dsaTarefaA deve ser executada antes de dsaTarefaB e dsaTarefaC
# dsaTarefaD deve ser executada após a conclusão de dsaTarefaB e dsaTarefaC
dsaTarefaA >> [dsaTarefaB, dsaTarefaC]
dsaTarefaD << [dsaTarefaB, dsaTarefaC]








