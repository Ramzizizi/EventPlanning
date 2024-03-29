from django.contrib import admin

from events import models as event_models


@admin.register(event_models.Event)
class EventAdmin(admin.ModelAdmin):
    """
    Отображение данные о мероприятии
    """

    # отображаемые параметры
    list_display = [
        "name",
        "organizer",
        "datetime_start",
        "datetime_end",
        "place",
    ]
    # поле для фильтрации
    list_filter = ["name"]
    # поле для поиска
    search_fields = ["name"]

    @admin.display(ordering="place__name", description="Организатор")
    def organizer(self, obj: event_models.Event):
        """
        Получение имени создателя ивента
        """
        return obj.organizer.username

    @admin.display(description="Место проведения")
    def place(self, obj: event_models.Event):
        """
        Получение имени места проведения
        """
        return obj.place.name

    def save_model(self, request, obj: event_models.Event, form, change):
        """
        Получения юзера
        """
        # получение юзера который создаёт модель
        obj.organizer = request.user
        # создание модели
        super().save_model(request, obj, form, change)
