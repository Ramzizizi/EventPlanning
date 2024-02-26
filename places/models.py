from django.db import models


class ActiveManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Place(models.Model):
    """
    Модель места
    """

    # базовые параметры места
    seat_capacity = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_places = ActiveManager()

    def __str__(self):
        return self.name


class Room(Place):
    """
    Модель комнаты
    """

    # добавление полей
    sofa_count = models.IntegerField(default=0)
    seat_count = models.IntegerField(default=0)


class Auditorium(Place):
    """
    Модель зала
    """

    # добавление полей
    mico_count = models.IntegerField(default=0)
    projects_count = models.IntegerField(default=0)
    entrances_count = models.IntegerField(default=0)
