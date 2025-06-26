from airflow.providers.google.cloud.operators.cloud_run import \
    CloudRunJobRunOperator


def run_cloud_run_job(project_id, region, job_name):
    return CloudRunJobRunOperator(
        task_id=f"run_job_{job_name}",
        project_id=project_id,
        region=region,
        job_name=job_name,
        wait=True,
    )
