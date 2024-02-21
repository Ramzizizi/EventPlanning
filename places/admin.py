from django.contrib import admin

from events import models as model_events
from places import models as model_places


class EventInline(admin.StackedInline):
    model = model_events.Event
    extra = 0


@admin.register(model_places.Room, model_places.Auditorium)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "seat_capacity")
    inlines = [EventInline]
