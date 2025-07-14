import traceback
from airflow.models import BaseOperator
from airflow.utils.email import send_email
from airflow.utils.decorators import apply_defaults


class BaseSafeOperator(BaseOperator):
    """
    Operator base com tratamento de erro e envio de email padronizado.
    As subclasses devem implementar o método `run_safe(context)`.
    """

    def __init__(self, alert_email=None, **kwargs):
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
                send_email(to=self.alert_email, subject=f"Erro no Airflow - {self.task_id}", html_content=error_msg.replace("\n", "<br>"))

            raise  # Relevanta exceção para o Airflow marcar como falha

    def run_safe(self, context):
        """
        Deve ser implementado pela subclasse.
        """
        raise NotImplementedError("Subclasses devem implementar o método run_safe()")
