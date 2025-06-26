from airflow.providers.google.cloud.operators.functions import (
    CloudFunctionInvokeFunctionOperator,
)


def invoke_cloud_function(project_id, location, function_name, data=None):
    return CloudFunctionInvokeFunctionOperator(
        task_id=f"invoke_function_{function_name}",
        project_id=project_id,
        location=location,
        input_data=data,
        function_id=function_name,
    )
