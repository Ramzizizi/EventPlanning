from django.contrib import admin

from . import models


class RoomInline(admin.StackedInline):
    """
    Класс доп. данных об ивенте для комнаты
    """

    # задание модели
    model = models.Event
    # задание количества предлагаемых для создания моделей
    extra = 0


class MeetingRoomInline(admin.StackedInline):
    """
    Класс доп. данных об ивенте для зала
    """

    # задание модели
    model = models.Event
    # задание количества предлагаемых для создания моделей
    extra = 0


class RoomAdmin(admin.ModelAdmin):
    """
    Отображение данные о комнате
    """

    # отображаемые параметры
    list_display = (
        "name",
        "seat_capacity",
        "sofa_count",
        "seat_count",
    )
    # дополнительные параметры
    inlines = [RoomInline]


class EventAdmin(admin.ModelAdmin):
    """
    Отображение данные об ивенте
    """

    # отображаемые параметры
    list_display = ("name", "organizer", "start", "end", "place")

    def organizer(self, obj: models.Event):
        """
        Получение имени создателя ивента
        """
        return obj.organizer.username

    def place(self, obj: models.Event):
        """
        Получение имени места проведения
        """
        if obj.room is not None:
            return obj.room.name
        else:
            return obj.meeting_room.name

    def save_model(self, request, obj: models.Event, form, change):
        """
        Получения юзера
        """
        # получение юзера который создаёт модель
        obj.organizer = request.user
        # создание модели
        super().save_model(request, obj, form, change)


# регистрация моделей и их отображения
admin.site.register(models.CustomUser)
admin.site.register(models.Room, RoomAdmin)
admin.site.register(models.MeetingRoom)
admin.site.register(models.Event, EventAdmin)
