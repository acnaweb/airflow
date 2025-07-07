from airflow.providers.google.cloud.operators.functions import CloudFunctionInvokeFunctionOperator


def invoke_cloud_function(project_id, location, function_name, data=None, task_id=None, **kwargs):
    """
    Cria uma task do Airflow para invocar uma Cloud Function no GCP.
    Permite customizar o task_id e passar argumentos extras para o operador.
    """
    return CloudFunctionInvokeFunctionOperator(
        task_id=task_id or f"invoke_function_{function_name}",
        project_id=project_id,
        location=location,
        input_data=data,
        function_id=function_name,
        **kwargs
    )
