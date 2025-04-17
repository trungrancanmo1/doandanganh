from celery import Celery

# Initialize Celery with Redis as broker
celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"  # Optional result backend
)

@celery.task
def add(x, y):
    return x + y