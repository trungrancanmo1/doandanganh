from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


from capp import celery
from .phase2 import phase2


# =================================================
# PHASE 1 TASK
# =================================================
@celery.task(name='phases.phase1')
def phase1(data):
    logger.info('Starting Phase 1...')
    # doing something
    logger.info('Finished Phase 1.')
    phase2.delay(data)