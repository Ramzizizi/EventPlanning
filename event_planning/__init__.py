from event_planning.event_celery import app as celery_app

# инициализация Celery приложения
__all__ = ("celery_app",)
