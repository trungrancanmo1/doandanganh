from celery import Celery

from mqtt_kafka_bridge.utils.config import MESSAGE_BROKER


celery = Celery(
    main='capp',
    broker=MESSAGE_BROKER,
    include=['mqtt_kafka_bridge.core.phases.phase1']
)


# celery.conf.update(
#     task_serializer="json",
#     result_serializer="json",
#     accept_content=["json"]
# )