from app.tasks.conf_celery import celery_worker

@celery_worker.task
def periodic_task():
    pass