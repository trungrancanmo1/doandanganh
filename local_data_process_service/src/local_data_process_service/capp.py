from celery import Celery

from local_data_process_service.utils.config import MESSAGE_BROKER


celery = Celery(
    main='capp',
    broker=MESSAGE_BROKER,
    include=['local_data_process_service.core.phases.phase1']
)


# celery.conf.update(
#     task_serializer="json",
#     result_serializer="json",
#     accept_content=["json"]
# )