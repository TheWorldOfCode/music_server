from celery import current_app as current_celery_app

def make_celery(app):
    celery = current_celery_app
    celery.config_from_object(app.config, namespace="CELERY")
    celery.conf.update(result_extended=True)
    return celery