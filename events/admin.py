from django.contrib import admin

from .models import Event


class EventAdmin(admin.ModelAdmin):
    """
    Отображение данные о мероприятии
    """

    # отображаемые параметры
    list_display = ("name", "organizer", "start", "end", "place")

    def organizer(self, obj: Event):
        """
        Получение имени создателя ивента
        """
        return obj.organizer.username

    def place(self, obj: Event):
        """
        Получение имени места проведения
        """
        return obj.place.name

    def save_model(self, request, obj: Event, form, change):
        """
        Получения юзера
        """
        # получение юзера который создаёт модель
        obj.organizer = request.user
        # создание модели
        super().save_model(request, obj, form, change)


admin.site.register(Event, EventAdmin)
