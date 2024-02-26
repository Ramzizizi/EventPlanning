from django.contrib import admin

from events import models as model_events
from places import models as model_places


class EventInline(admin.StackedInline):
    model = model_events.Event
    extra = 0


@admin.register(model_places.Room, model_places.Auditorium)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "seat_capacity", "is_active")
    inlines = [EventInline]

    actions = ["deactivate", "activate"]

    @admin.action(description="Deactivate place")
    def deactivate(self, request, queryset):
        queryset.update(is_active=0)

    @admin.action(description="Active place")
    def activate(self, request, queryset):
        queryset.update(is_active=1)
