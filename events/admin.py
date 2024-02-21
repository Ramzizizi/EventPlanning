from django.contrib import admin

from events import models as model_events


@admin.register(model_events.Event)
class EventAdmin(admin.ModelAdmin):
    """
    Отображение данные о мероприятии
    """

    # отображаемые параметры
    list_display = ("name", "organizer", "start", "end", "place")
    list_filter = ["name"]
    search_fields = ["name"]

    @admin.display(ordering="place__name")
    def organizer(self, obj: model_events.Event):
        """
        Получение имени создателя ивента
        """
        return obj.organizer.username

    def place(self, obj: model_events.Event):
        """
        Получение имени места проведения
        """
        return obj.place.name

    def save_model(self, request, obj: model_events.Event, form, change):
        """
        Получения юзера
        """
        # получение юзера который создаёт модель
        obj.organizer = request.user
        # создание модели
        super().save_model(request, obj, form, change)
