import os
import logging
import requests
from airflow.decorators import dag, task
from airflow.providers.google.common.hooks.base_google import GoogleBaseHook
from google.auth import default
from google.auth.transport.requests import Request
from airflow.models.variable import Variable
from airflow.utils.context import Context
import jsonpath_ng.ext as jp

# Configuração de logging centralizada
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configurações do GCP
GOOGLE_CLOUD_REGION = Variable.get("GOOGLE_CLOUD_REGION")
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", None)

if GOOGLE_CLOUD_PROJECT is None:
    GOOGLE_CLOUD_PROJECT = Variable.get("GOOGLE_CLOUD_PROJECT")

BASE_URL = f"https://run.googleapis.com/v2/projects/{GOOGLE_CLOUD_PROJECT}/locations/{GOOGLE_CLOUD_REGION}/jobs"

JOBS = {
    "job1": "job1",
    "job2": "job2",
}


def build_payload(data: dict) -> dict:
    """Constrói o payload  de job do Cloud Run."""
    return {
        "overrides": {
            "containerOverrides": [
                {
                    "args": [
                        "python",
                        "src/main.py",
                        data["arg1"],
                        data["arg2"]
                    ]
                }
            ]
        }
    }


def get_token_composer() -> str:
    """Obtém o token para autenticação no Composer."""
    credentials, project = default()
    credentials.refresh(Request())
    return credentials.token


def get_token_airflow() -> str:
    """Obtém o token para autenticação no Airflow."""
    hook = GoogleBaseHook(gcp_conn_id="gcp")
    credentials = hook.get_credentials()
    credentials.refresh(Request())
    logger.info(credentials.token)
    return credentials.token


def get_headers() -> dict:
    """Obtém os cabeçalhos de autenticação para chamadas à API do Cloud Run."""
    token = (
        get_token_airflow()
        if os.getenv("GOOGLE_CLOUD_PROJECT", None) is None
        else get_token_composer()
    )
    return {"Authorization": f"Bearer {token}"}


def get_execution_id(data: dict) -> str:
    """Extrai o ID de execução do JSON de resposta da API."""
    expression = jp.parse("$.metadata.name")
    result = [match.value for match in expression.find(data)]
    return result[0] if result else ""


def get_execution_state(data: dict) -> str:
    """Extrai o estado da execução do JSON de resposta da API."""
    expression = jp.parse("$.conditions[?(@.type == 'Completed')].state")
    states = [match.value for match in expression.find(data)]
    return states[0] if states else "UNKNOWN"


# Definição padrão para o DAG
default_args = {
    "owner": "airflow",
    "retries": 0,
}


@dag(
    default_args=default_args,
    schedule_interval=None,
    start_date=None,
    catchup=False,
    tags=["jobs", "monitoramento"],
)
def dag_etl():
    @task
    def process_conf(**context):
        """
        Função que processa as configurações enviadas para a DAG.
        """
        dag_run = context.get("dag_run")
        if dag_run and dag_run.conf:
            data = dag_run.conf
            logger.info(f"Configurações recebidas: {data}")
            context["ti"].xcom_push(key="data", value=data)
        else:
            raise Exception("Nenhuma configuração recebida.")

    def create_execution(job_name: str, payload: dict) -> str:
        """Inicia um job no Cloud Run e retorna o execution_id."""
        url = f"{BASE_URL}/{job_name}:run"
        try:
            response = requests.post(url, headers=get_headers(), json=payload)
            response.raise_for_status()
            execution_id = get_execution_id(response.json())
            logger.info(f"Job {job_name} iniciado com execution_id: {execution_id}")
            return execution_id
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao iniciar job {job_name}: {e}")
            raise

    def monitor_execution(execution_id: str) -> bool:
        """Monitora o status de um job no Cloud Run."""
        url = f"https://run.googleapis.com/v2/{execution_id}"
        try:
            response = requests.get(url, headers=get_headers())
            response.raise_for_status()
            state = get_execution_state(response.json())
            logger.info(f"Status da execução {execution_id}: {state}")
            return state in ["CONDITION_FAILED", "CONDITION_SUCCEEDED"]
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao monitorar job {execution_id}: {e}")
            raise

    @task
    def start_job1(task_instance: Context):
        """Inicia o job  no Cloud Run."""
        data = task_instance.xcom_pull(task_ids="process_conf", key="data")
        payload = build_payload(data)
        execution_id = create_execution(JOBS["job1"], payload)
        task_instance.xcom_push(key="job1_id", value=execution_id)

    @task.sensor(poke_interval=20, timeout=5400)
    def wait_job1(task_instance: Context):
        """Monitora a execução do preprocessor."""
        execution_id = task_instance.xcom_pull(
            task_ids="start_job1", key="job1_id"
        )
        return monitor_execution(execution_id)

    # Fluxo de execução do DAG
    (
        process_conf()
        >> start_job1()
        >> wait_job1()
    )


dag_etl()
