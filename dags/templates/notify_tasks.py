import requests

from airflow.operators.email import EmailOperator
from airflow.operators.python import PythonOperator
from airflow.providers.slack.operators.slack_api import SlackAPIPostOperator


def slack_notify(channel, message, slack_conn_id="slack_default"):
    return SlackAPIPostOperator(
        task_id="notify_slack",
        token="{{ var.value.slack_token }}",
        text=message,
        channel=channel,
    )


def email_notify(to, subject, html_content):
    return EmailOperator(
        task_id="notify_email", to=to, subject=subject, html_content=html_content
    )


def datadog_event(title, text, alert_type="info"):
    def _send():
        api_key = "{{ var.value.datadog_api_key }}"
        payload = {"title": title, "text": text, "alert_type": alert_type}
        requests.post(
            "https://api.datadoghq.com/api/v1/events",
            headers={"DD-API-KEY": api_key},
            json=payload,
        )

    return PythonOperator(task_id="notify_datadog", python_callable=_send)
