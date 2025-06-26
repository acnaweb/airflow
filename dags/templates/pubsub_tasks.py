from airflow.providers.google.cloud.operators.pubsub import PubSubPublishMessageOperator


def publish_message(topic, messages):
    return PubSubPublishMessageOperator(
        task_id=f"publish_to_{topic}", topic=topic, messages=messages
    )
