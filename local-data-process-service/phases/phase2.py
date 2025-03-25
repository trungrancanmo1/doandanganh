from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


from capp import celery


@celery.task(name='phases.phase2')
def phase2(data):
    logger.info('Starting Phase 2...')
    # doing something
    logger.info('Finished Phase 2.')