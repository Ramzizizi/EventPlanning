from django.db import models

from places import validators as place_validators


class ActiveManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Place(models.Model):
    """
    Модель места
    """

    # базовые параметры места
    seat_capacity = models.PositiveIntegerField(
        default=0,
        verbose_name="Вместимость",
        validators=[place_validators.positive_integer_validator],
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активное",
    )

    objects = models.Manager()
    active_places = ActiveManager()

    def __str__(self):
        return self.name


class Room(Place):
    """
    Модель комнаты
    """

    # добавление полей
    sofa_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество диванов",
        validators=[place_validators.positive_integer_validator],
    )
    seat_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Сидячих мест",
        validators=[place_validators.positive_integer_validator],
    )

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"


class Auditorium(Place):
    """
    Модель зала
    """

    # добавление полей
    mico_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количеств микрофонов",
        validators=[place_validators.positive_integer_validator],
    )
    projects_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество проекторов",
        validators=[place_validators.positive_integer_validator],
    )
    entrances_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество входов",
        validators=[place_validators.positive_integer_validator],
    )

    class Meta:
        verbose_name = "Аудитория"
        verbose_name_plural = "Аудитории"
