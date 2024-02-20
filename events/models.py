import enum
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import localtime

from users import models as user_models
from places import models as place_models


class EventStatus(enum.Enum):
    AVAILABLE_EVENT = 1
    PASS_EVENT = 2


class Event(models.Model):
    """
    Модель мероприятия
    """

    objects = models.Manager()

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
        related_name="Visitor",
        verbose_name="Посетители",
    )

    event_capacity = models.IntegerField(
        default=0, verbose_name="Количество участников",
    )

    start = models.DateTimeField(
        "Время начала",
        blank=False,
        null=False,
    )

    end = models.DateTimeField("Время конца", blank=False, null=False)

    place: place_models.Place = models.ForeignKey(
        place_models.Place,
        on_delete=models.CASCADE,
        verbose_name="Место провидения",
    )

    msg_distribute = models.BooleanField(
        blank=True, default=False, auto_created=True
    )

    @property
    def event_visitors_count(self) -> int:
        return self.visitors.count()

    @property
    def free_capacity(self) -> int:
        return self.event_capacity - self.event_visitors_count

    @property
    def event_status(self):
        time_now = localtime()

        if self.start < time_now:
            if self.end < time_now:
                return EventStatus.PASS_EVENT
            return EventStatus.AVAILABLE_EVENT

        return EventStatus.AVAILABLE_EVENT

    # функция вызывающая при сохранении для валидации введенных данных
    def clean(self):
        """
        Валидация уже введенных данных
        """
        if not self.event_capacity:
            raise ValidationError("Need visitors")
        if type(self.end) != datetime or type(self.start) != datetime:
            raise ValidationError("Start or end is not correct datetime")
        # проверка начала и конца ивента
        if self.end < self.start:
            raise ValidationError("Event end can't be newer the he start")
        # проверка соответствия текущему времени
        if self.end < localtime():
            raise ValidationError(
                "Event end can't be older than the current date and time"
            )
        if self.start < localtime():
            raise ValidationError(
                "Event start can't be older than the current date and time"
            )
        # проверка на кол-во свободных мест в комнате
        events = (
            Event.objects.filter(place__pk=self.place.pk)
            .exclude(pk=self.pk)
            .all()
        )
        events = [
            event for event in events if event.start <= self.start <= event.end
        ]
        events_capacity = sum(event.event_capacity for event in events)
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
                    models.Q(start__isnull=False, end__isnull=False)
                    | models.Q(start__isnull=True, end__isnull=False)
                    | models.Q(start__isnull=False, end__isnull=True)
                ),
            ),
        ]
