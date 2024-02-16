from datetime import timedelta
from time import sleep

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
        time_for_sleep = timedelta(minutes=1).seconds
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
                    if (next_event.start - localtime()).seconds - timedelta(
                        hours=1
                    ).seconds:
                        logger.info("Start check emails for send msgs")
                        visitors = next_event.visitors.all()
                        emails = [i.email for i in visitors]
                        if emails:
                            logger.info(f"Send msg to: {emails}")
                            send_mail(
                                "Уведомление",
                                f"В {next_event.start.__str__()} у вас будет мероприятие.",
                                "admin@test.com",
                                emails,
                                fail_silently=True,
                            )
                        time_for_sleep = timedelta(minutes=1).seconds
                    else:
                        time_for_sleep = (
                            next_event.start - localtime()
                        ).seconds - timedelta(hours=1).seconds
                    logger.info(f"Wait next event: {time_for_sleep} seconds")
                else:
                    logger.info(f"Wait {time_for_sleep} seconds")
            else:
                time_for_sleep = (event.start - localtime()).seconds - timedelta(
                    hours=1
                ).seconds
                logger.info(f"Wait next event: {time_for_sleep} seconds")
        else:
            logger.info(f"Wait {time_for_sleep} seconds")
        sleep(time_for_sleep)
