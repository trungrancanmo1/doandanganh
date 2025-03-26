from firebase import firestore_db
from concurrent.futures import ThreadPoolExecutor
from .logger import logger
import queue


data_queue = queue.Queue()


def process_record(record):
    '''
    - Persist data to the FluxDb
    '''
    try:
        feed_id = record.get('feed_id')
        firestore_db\
        .collection('sensors', feed_id, 'records')\
        .add(record, str(record['timestamp']))

        logger.info(f'Persist data from {feed_id}')
    except Exception as e:
        logger.error(f'Failed to persist data: {e}')


def worker():
    '''
    - The worker of the threads pool
    - Continuously access the queue (thread-safe) and process data
    '''
    while True:
        record = data_queue.get()
        # process_record(record)
        logger.info(f'Process {record}')
        data_queue.task_done()