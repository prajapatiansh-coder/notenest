from celery import Celery

def create_celery(app_name):
    return Celery(app_name)

celery = create_celery('campus_notes')
