from celery import Celery

from config.config import MESSAGE_BROKER



celery = Celery(
    main='capp',
    broker=MESSAGE_BROKER,
    include=['phases.phase1', 'phases.phase2']
)


# celery.conf.update(
#     task_serializer="json",
#     result_serializer="json",
#     accept_content=["json"]
# )