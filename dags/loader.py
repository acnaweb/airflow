import os
from gusty import create_dag
from airflow.models import Variable



def current_env() -> str:
    """
    Lê o ambiente a partir da Airflow Variable 'env' e valida.
    Aceita: dev | stg | prd
    """
    value = Variable.get("env", default_var=None)
    if not value:
        raise RuntimeError(
            "Airflow Variable 'env' não encontrada. "
            "Crie-a em Admin > Variables com um dos valores: dev, stg ou prd."
        )
    value = value.strip().lower()
    if value not in {"dev", "stg", "prd"}:
        raise RuntimeError(
            f"Valor inválido para Variable 'env': {value!r}. "
            "Use um dos valores: dev, stg, prd."
        )
    return value


#####################
## DAG Directories ##
#####################

env = current_env()
# point to your dags directory
dag_parent_dir = os.path.join(os.environ['AIRFLOW_HOME'], "dags", env)

# assumes any subdirectories in the dags directory are Gusty DAGs (with METADATA.yml) (excludes subdirectories like __pycache__)
dag_directories = [os.path.join(dag_parent_dir, name) for name in os.listdir(dag_parent_dir) if os.path.isdir(os.path.join(dag_parent_dir, name)) and not name.endswith('__')]

####################
## DAG Generation ##
####################


for dag_directory in dag_directories:
    dag_id = os.path.basename(dag_directory)

    globals()[dag_id] = create_dag(dag_directory,
                                   description="[Atenção] Incluir a descrição",
                                   default_args={
                                        "owner": "data-eng"
                                   },                                   
                                   catchup=False,
                                   extra_tags = [f'env:{env}'],                                                                      
                                   latest_only=False)