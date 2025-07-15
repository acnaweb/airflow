import os
import traceback
from airflow.models import BaseOperator
from airflow.utils.email import send_email
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from google.cloud import storage


class BaseSafeOperator(BaseOperator):
    """
    Operator base com:
    - Tratamento de erro com log estruturado
    - Envio de email em caso de falha
    - Autenticação inteligente com GCP (GOOGLE_APPLICATION_CREDENTIALS ou gcp_conn_id)

    Subclasses devem sobrescrever o método run_safe(context).
    """

    def __init__(
        self,
        alert_email: str = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.alert_email = alert_email

    def execute(self, context):
        try:
            return self.run_safe(context)
        except Exception as e:
            error_msg = f"""
            ❌ Task {self.task_id} falhou no DAG {context.get('dag_id', self.dag_id)}
            📅 Execução: {context.get('ds', 'N/A')}
            📄 Erro: {str(e)}
            🔍 Traceback:
            {traceback.format_exc()}
            """
            self.log.error(error_msg)

            if self.alert_email:
                self.log.info(f"Enviando email de erro para: {self.alert_email}")
                send_email(
                    to=self.alert_email,
                    subject=f"[Airflow] Erro na task: {self.task_id}",
                    html_content=error_msg.replace("\n", "<br>")
                )

            raise

    def run_safe(self, context):
        """
        Deve ser sobrescrito por subclasses.
        """
        raise NotImplementedError("Subclasses devem implementar o método run_safe().")

