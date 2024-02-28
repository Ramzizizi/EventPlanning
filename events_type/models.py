from django.db import models

from users import models as user_models


class EventType(models.Model): ...


class ConfCall(EventType):
    call_url = models.URLField(
        blank=False,
        null=False,
        verbose_name="Ссылка на конференцию",
    )

    class Meta:
        verbose_name = "Конференц-звонок"
        verbose_name_plural = "Конференц-звонки"


class Meeting(EventType):
    need_visit = models.BooleanField(
        default=True,
        blank=False,
        null=False,
        verbose_name="Необходимость посещения",
    )
    theme = models.TextField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Тема собрания",
    )

    class Meta:
        verbose_name = "Собрание"
        verbose_name_plural = "Собрания"


class Conference(EventType):
    speakers = models.ManyToManyField(
        user_models.Speaker,
        verbose_name="Спикеры",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Конференция"
        verbose_name_plural = "Конференции"
