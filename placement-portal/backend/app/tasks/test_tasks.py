from app.celery_app import celery


@celery.task
def add_numbers(a, b):

    return a + b