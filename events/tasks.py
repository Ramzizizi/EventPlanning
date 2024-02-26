from datetime import timedelta
from time import sleep

from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from django.utils.timezone import localtime

from event_planning.settings import (
    PRE_EVENT_TIME_SECONDS,
    PERIOD_NOTIFICATION_SECONDS,
    FROM_EMAIL,
)
from event_planning.event_celery import app
from events import models as model_events


logger = get_task_logger(__name__)


@app.task
def debug_task():
    """
    Задача для рассылки уведомлений
    """
    logger.info("Task start")
    while True:
        # получаем мероприятия на день для которых не было произведено рассылки
        events = (
            model_events.Event.event_object.exclude(msg_distribute=1)
            .filter(
                msg_distribute=False,
                start__gte=localtime(),
                start__lte=localtime()
                + timedelta(hours=PRE_EVENT_TIME_SECONDS),
            )
            .order_by("start")
            .all()
        )
        logger.info(f"Find events: {events}")
        # обрабатываем все мероприятия
        for event in events:
            logger.info(f"Start send msgs for event: {event.name}")
            visitors = event.visitors.all()
            # получаем список почт для рассылки
            visitor_emails = [visitor.email for visitor in visitors]
            logger.info(f"Visitors list: {visitor_emails}")
            # отправляем сообщения
            send_mail(
                "Уведомление",
                f"В {event.start.__str__()} у вас будет мероприятие.",
                FROM_EMAIL,
                visitor_emails,
                fail_silently=True,
            )
            # устанавливаем статус произведенной рассылки
            event.msg_distribute = True
            event.save()
            logger.info(f"End send msgs for event: {event.name}")
        logger.info(f"Wait {PERIOD_NOTIFICATION_SECONDS} seconds")
        # ожидание заданного времени
        sleep(PERIOD_NOTIFICATION_SECONDS)
