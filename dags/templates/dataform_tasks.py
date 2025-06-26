from airflow.providers.google.cloud.operators.dataform import (
    DataformCreateCompilationResultOperator,
    DataformCreateWorkflowInvocationOperator,
)


def compile_dataform(project_id, region, repo_name, branch="main"):
    return DataformCreateCompilationResultOperator(
        task_id="compile_dataform",
        project_id=project_id,
        region=region,
        repository_id=repo_name,
        git_commitish=branch,
    )


def run_dataform_workflow(project_id, region, repo_name, compilation_result):
    return DataformCreateWorkflowInvocationOperator(
        task_id="run_dataform_workflow",
        project_id=project_id,
        region=region,
        repository_id=repo_name,
        compilation_result_id=compilation_result,
    )
