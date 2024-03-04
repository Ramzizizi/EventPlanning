from django.db import models

from users import models as user_models


class EventType(models.Model):
    objects = models.Manager()


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
    meeting_theme = models.TextField(
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
        user_models.CustomUser,
        verbose_name="Спикеры",
        through="Themes",
        blank=True,
    )

    class Meta:
        verbose_name = "Конференция"
        verbose_name_plural = "Конференции"


class Themes(models.Model):

    objects = models.Manager()

    event: Conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
    )
    speaker: user_models.CustomUser = models.ForeignKey(
        user_models.CustomUser,
        on_delete=models.CASCADE,
        related_name="Speaker",
        verbose_name="Спикер",
    )
    theme = models.TextField(
        max_length=255,
        verbose_name="Тема выступления",
    )

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"
