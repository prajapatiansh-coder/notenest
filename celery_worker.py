import os
from app import create_app
from app.worker import celery

app = create_app()

# Initialize celery with app config
celery.conf.update(app.config)

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask
