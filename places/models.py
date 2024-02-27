from django.db import models


class ActiveManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Place(models.Model):
    """
    Модель места
    """

    # базовые параметры места
    seat_capacity = models.IntegerField(
        default=0,
        verbose_name="Вместимость",
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
    sofa_count = models.IntegerField(
        default=0,
        verbose_name="Количество диванов",
    )
    seat_count = models.IntegerField(
        default=0,
        verbose_name="Сидячих мест",
    )

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"


class Auditorium(Place):
    """
    Модель зала
    """

    # добавление полей
    mico_count = models.IntegerField(
        default=0,
        verbose_name="Количеств микрофонов",
    )
    projects_count = models.IntegerField(
        default=0,
        verbose_name="Количество проекторов",
    )
    entrances_count = models.IntegerField(
        default=0,
        verbose_name="Количество входов",
    )

    class Meta:
        verbose_name = "Аудитория"
        verbose_name_plural = "Аудитории"
