from celery import shared_task
from time import sleep
from todo.models import Task
import logging

logger = logging.getLogger(__name__)

@shared_task
def sendEmail():
    sleep(3)
    print('done sending email')
    
    


@shared_task
def deleteTask():
    completed_tasks = Task.objects.filter(complete=True)
    count = completed_tasks.count()
    logger.info(f"Found {count} completed tasks to delete.")
    deleted_count, _ = completed_tasks.delete()
    logger.info(f"{deleted_count} completed tasks deleted.")
    return deleted_count
