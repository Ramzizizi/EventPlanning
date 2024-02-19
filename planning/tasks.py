from datetime import timedelta
from time import sleep

from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from django.utils.timezone import localtime

from event_planning.event_celery import app
from planning import models

logger = get_task_logger(__name__)

# константы для задачи
SECONDS_FOR_WAIT = 1800
PRE_EVENT_TIME_SECONDS = 3600
FROM_EMAIL = "admin@test.com"


@app.task
def debug_task():
    logger.info("Task start")
    while True:
        # получаем ближайшие 2 мероприятия
        events = (
            models.Event.objects.exclude(event_status=1)
            .filter(
                msg_distribute=False,
                start__gte=localtime(),
                start__lte=localtime() + timedelta(hours=PRE_EVENT_TIME_SECONDS),
            )
            .order_by("start")
            .all()
        )
        logger.info(f"Find events: {events}")
        # обрабатываем первое мероприятие
        for event in events:
            logger.info(f"Start send msgs for event: {event.name}")
            visitors = event.visitors.all()
            # получаем список почт для рассылки
            visitor_emails = [visitor.email for visitor in visitors]
            logger.info(f"Visitors list: {visitor_emails}")
            send_mail(
                "Уведомление",
                f"В {event.start.__str__()} у вас будет мероприятие.",
                FROM_EMAIL,
                visitor_emails,
                fail_silently=True,
            )
            event.msg_distribute = True
            event.save()
            logger.info(f"End send msgs for event: {event.name}")
        logger.info(f"Wait {SECONDS_FOR_WAIT} seconds")
        sleep(SECONDS_FOR_WAIT)
