import os

from celery import Celery
from celery.signals import worker_ready


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_planning.settings")
app = Celery("event_planning")
app.config_from_object(
    "django.conf:settings", namespace="CELERY"
)
app.autodiscover_tasks()


@worker_ready.connect
def at_start(sender, **k):
    """
    Запуск задачи при старте Celery
    """
    with sender.app.connection() as conn:
        sender.app.send_task(
            "events.tasks.debug_task", connection=conn
        )
