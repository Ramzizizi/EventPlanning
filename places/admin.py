from django.contrib import admin

from events import models as model_events
from places import models as model_places


class EventInline(admin.StackedInline):
    model = model_events.Event
    extra = 0


class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "seat_capacity")
    inlines = [EventInline]


# регистрация моделей и их отображения
admin.site.register(model_places.Room, PlaceAdmin)
admin.site.register(model_places.Auditorium, PlaceAdmin)
