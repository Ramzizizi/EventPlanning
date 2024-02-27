import enum
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum, Count, Q
from django.db.models.functions import Coalesce
from django.utils.timezone import localtime

from users import models as user_models
from places import models as place_models


class EventStatus(enum.Enum):
    UPCOMING = 1
    IN_PROGRESS = 2
    PASSED = 3


class EventManager(models.Manager):

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(count=Coalesce(Count("visitors"), 0))
        )


class Event(models.Model):
    """
    Модель мероприятия
    """

    event_object = EventManager()

    # задание параметров
    name = models.CharField(max_length=255, verbose_name="Название")

    organizer: user_models.CustomUser = models.ForeignKey(
        user_models.CustomUser,
        on_delete=models.CASCADE,
        editable=False,
        related_name="Organizer",
        verbose_name="Организатор",
    )

    visitors: user_models.CustomUser = models.ManyToManyField(
        user_models.CustomUser,
        blank=True,
        related_name="Visitor",
        verbose_name="Посетители",
    )

    event_capacity = models.IntegerField(
        default=0,
        verbose_name="Количество участников",
    )

    datetime_start = models.DateTimeField(
        "Время начала",
        blank=False,
        null=False,
    )

    datetime_end = models.DateTimeField("Время конца", blank=False, null=False)

    place: place_models.Place = models.ForeignKey(
        place_models.Place,
        on_delete=models.CASCADE,
        verbose_name="Место провидения",
    )

    msg_distribute = models.BooleanField(
        blank=True,
        default=False,
        auto_created=True,
        editable=False,
    )

    @property
    def free_capacity(self) -> int:
        return (
            self.event_capacity
            - Event.event_object.filter(pk=self.pk).first().count
        )  # type: ignore

    @property
    def event_status(self):
        time_now = localtime()

        if self.datetime_start < time_now:
            if self.datetime_end < time_now:
                return EventStatus.PASSED
            return EventStatus.IN_PROGRESS

        return EventStatus.UPCOMING

    def clean(self):
        """
        Валидация уже введенных данных
        """
        if not self.event_capacity:
            raise ValidationError("Need visitors")
        if (
            type(self.datetime_end) is not datetime
            or type(self.datetime_start) is not datetime
        ):
            raise ValidationError("Start or end is not correct datetime")
        # проверка начала и конца ивента
        if self.datetime_end < self.datetime_start:
            raise ValidationError("Event end can't be newer the he start")
        # проверка соответствия текущему времени
        if self.datetime_end < localtime():
            raise ValidationError(
                "Event end can't be older than the current date and time"
            )
        if self.datetime_start < localtime():
            raise ValidationError(
                "Event start can't be older than the current date and time"
            )
        # проверка на кол-во свободных мест в комнате
        events_capacity = (
            Event.event_object.filter(
                Q(place__pk=self.place.pk)
                & (
                    Q(datetime_start__lte=self.datetime_start)
                    & Q(datetime_end__gte=self.datetime_start)
                )
                | (
                    Q(datetime_start__lte=self.datetime_end)
                    & Q(datetime_end__gte=self.datetime_end)
                )
            )
            .exclude(pk=self.pk)
            .aggregate(sum=Coalesce(Sum("event_capacity"), 0))
        )["sum"]
        if (self.place.seat_capacity - events_capacity) < self.event_capacity:
            raise ValidationError("Event capacity bigger then place capacity")

    def __str__(self):
        return self.name

    class Meta:
        """
        Определение мета-данных модели
        """

        # задание необходимых параметров
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_start_or_end_time",
                check=(
                    models.Q(
                        datetime_start__isnull=False, datetime_end__isnull=False
                    )
                    | models.Q(
                        datetime_start__isnull=True, datetime_end__isnull=False
                    )
                    | models.Q(
                        datetime_start__isnull=False, datetime_end__isnull=True
                    )
                ),
            ),
        ]
