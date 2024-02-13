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


class Place(models.Model):
    """
    Модель места
    """

    # базовые параметры места
    seat_capacity = models.IntegerField(default=0)
    name = models.CharField(max_length=100)


class Room(Place):
    """
    Моедль комнаты
    """

    # добавление полей
    sofa_count = models.IntegerField(default=0)
    seat_count = models.IntegerField(default=0)

    # создание параметра
    @property
    def free_capacity(self):
        """
        Функция подсчёта свободных мест в комнате
        """
        # получение всех ивентов в этой комнате
        events = Event.objects.filter(room__pk=self.pk).all()
        # нахождение числа свободных мест
        return self.seat_capacity - sum(i.event_capacity for i in events)


class MeetingRoom(Place):
    """
    Модель зала
    """

    # добавление полей
    mico_count = models.IntegerField(default=0)
    projects_count = models.IntegerField(default=0)
    entrances_count = models.IntegerField(default=0)

    # создание параметра
    @property
    def free_capacity(self):
        """
        Функция подсчёта свободных мест в комнате
        """
        # получение всех ивентов в этой комнате
        events = Event.objects.filter(meeting_room__pk=self.pk).all()
        # нахождение числа свободных мест
        return self.seat_capacity - sum(i.event_capacity for i in events)


class EventStatus(models.IntegerChoices):
    """
    Класс для определения состояния ивента
    """

    PastEvent = 1
    CurrentEvent = 2
    UpComingEvent = 3


class Event(models.Model):
    """
    Модель ивента
    """

    # задание параметров
    name = models.CharField(max_length=255)
    organizer: CustomUser = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, editable=False, related_name="Organizer"
    )
    visitors: CustomUser = models.ManyToManyField(
        CustomUser, related_name="Visitor", editable=False
    )
    event_capacity = models.IntegerField(default=0)
    start = models.DateTimeField("Start event date and time", blank=False, null=False)
    end = models.DateTimeField("End event date and time", blank=False, null=False)
    room: Room = models.ForeignKey(
        Room, on_delete=models.CASCADE, blank=True, null=True
    )
    meeting_room: MeetingRoom = models.ForeignKey(
        MeetingRoom, on_delete=models.CASCADE, blank=True, null=True
    )
    event_status: EventStatus = models.IntegerField(
        choices=EventStatus, default=EventStatus.UpComingEvent
    )

    # функция вызывающая при сохранении для валидации введенных данных
    def clean(self):
        """
        Валидация уже введенных данных
        """
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
        # проверка на кол-во свободных мест в комнате
        if self.room is not None:
            place = self.room
            events = Event.objects.filter(room__pk=place.pk).exclude(pk=self.pk).all()
        else:
            place = self.meeting_room
            events = Event.objects.filter(room__pk=place.pk).exclude(pk=self.pk).all()
        events_capacity = sum(i.event_capacity for i in events)
        if (place.seat_capacity - events_capacity) < self.event_capacity:
            raise ValidationError("Can't create event for this place")

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
