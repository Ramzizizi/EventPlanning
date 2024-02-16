import time
from datetime import timedelta

from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from django.utils.timezone import localtime

from event_planning.event_celery import app
from planning import models

logger = get_task_logger(__name__)


@app.task
def debug_task():
    logger.info("Task start")
    while True:
        logger.info(localtime())
        events = (
            models.Event.objects.exclude(event_status=1)
            .filter(start__gte=localtime())
            .order_by("start")
            .all()[0:2]
        )
        logger.info(events)
        event = events[0] if len(events) >= 1 else None
        next_event = events[1] if len(events) > 1 else None
        time_for_sleep = timedelta(minutes=30).seconds
        if event is not None:
            if (event.start - localtime()).seconds <= timedelta(hours=1).seconds:
                logger.info("Start check emails for send msgs")
                visitors = event.visitors.all()
                emails = [i.email for i in visitors]
                if emails:
                    logger.info(f"Send msg to: {emails}")
                    send_mail(
                        "Уведомление",
                        f"В {event.start.__str__()} у вас будет мероприятие.",
                        "admin@test.com",
                        emails,
                        fail_silently=True,
                    )
                else:
                    logger.info("No find emails for send")
                if next_event is not None:
                    time_for_sleep = (
                        next_event.start - localtime() - timedelta(hours=1)
                    ).seconds
                    logger.info(f"Wait next event: {time_for_sleep} seconds")
                else:
                    logger.info("Wait 30 minutes")
            else:
                time_for_sleep = (
                    event.start - localtime() - timedelta(hours=1)
                ).seconds
                logger.info(f"Wait next event: {time_for_sleep} seconds")
        else:
            logger.info("Wait 30 minutes")
        time.sleep(time_for_sleep)
