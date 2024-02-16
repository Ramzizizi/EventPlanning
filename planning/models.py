from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import localtime


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя
    """

    # инициализация полей
    username = models.TextField(max_length=255, unique=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_admin = models.BooleanField(default=False)

    # установка параметров полей
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username", "date_of_birth"]

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(
            ("pbkdf2_sha256$", "bcrypt$", "argon2")
        ):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Place(models.Model):
    """
    Модель места
    """

    # базовые параметры места
    seat_capacity = models.IntegerField(default=0)
    name = models.CharField(max_length=100)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Room(Place):
    """
    Модель комнаты
    """

    # добавление полей
    sofa_count = models.IntegerField(default=0)
    seat_count = models.IntegerField(default=0)


class MeetingRoom(Place):
    """
    Модель зала
    """

    # добавление полей
    mico_count = models.IntegerField(default=0)
    projects_count = models.IntegerField(default=0)
    entrances_count = models.IntegerField(default=0)


class EventStatus(models.IntegerChoices):
    """
    Класс для определения состояния ивента
    """

    NotActiveEvent = 1
    ActiveEvent = 2


class Event(models.Model):
    """
    Модель ивента
    """

    # задание параметров
    name = models.CharField(max_length=255, verbose_name="Название")
    organizer: CustomUser = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        editable=False,
        related_name="Organizer",
        verbose_name="Организатор",
    )
    visitors: CustomUser = models.ManyToManyField(
        CustomUser, related_name="Visitor", verbose_name="Посетители"
    )
    event_capacity = models.IntegerField(
        default=0, verbose_name="Количество участников"
    )
    start = models.DateTimeField(
        "Время начала",
        blank=False,
        null=False,
    )
    end = models.DateTimeField("Время конца", blank=False, null=False)
    room: Room = models.ForeignKey(
        Room, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Комната"
    )
    meeting_room: MeetingRoom = models.ForeignKey(
        MeetingRoom, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Зал"
    )
    event_status: EventStatus = models.IntegerField(
        choices=EventStatus,
        default=EventStatus.ActiveEvent,
        verbose_name="Статус мероприятия",
    )

    objects = models.Manager()

    @property
    def free_capacity(self):
        return self.event_capacity - self.visitors.count()

    @property
    def event_visitors_counts(self):
        return self.visitors.count()

    @property
    def check_status(self):
        if self.end < localtime():
            self.event_status = EventStatus.NotActiveEvent
            self.save()
        return None

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
                "Event end date and time can't be older than the current date and time"
            )
        if self.start < localtime():
            raise ValidationError(
                "Event start date and time can't be older than the current date and time"
            )
        if not (self.room is None and self.meeting_room is None):
            # проверка на кол-во свободных мест в комнате
            if self.room is not None:
                place = self.room
                events = (
                    Event.objects.filter(room__pk=place.pk).exclude(pk=self.pk).all()
                )
            else:
                place = self.meeting_room
                events = (
                    Event.objects.filter(meeting_room__pk=place.pk)
                    .exclude(pk=self.pk)
                    .all()
                )
            events = [i for i in events if i.start <= self.start <= i.end]
            events_capacity = sum(i.event_capacity for i in events)
            if (place.seat_capacity - events_capacity) < self.event_capacity:
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
                name="%(app_label)s_%(class)s_room_or_meeting_room",
                check=(
                    models.Q(room__isnull=True, meeting_room__isnull=False)
                    | models.Q(room__isnull=False, meeting_room__isnull=True)
                ),
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_start_or_end_time",
                check=(
                    models.Q(start__isnull=True, end__isnull=False)
                    | models.Q(start__isnull=False, end__isnull=False)
                    | models.Q(start__isnull=False, end__isnull=True)
                ),
            ),
        ]
