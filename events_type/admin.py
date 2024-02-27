from django.contrib import admin

from events import models as event_models
from events_type import models as event_type_models


class EventInline(admin.StackedInline):
    model = event_models.Event

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(
    event_type_models.Meeting,
    event_type_models.Conference,
    event_type_models.ConfCall,
)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ["name", "datetime_start", "datetime_end", "place"]

    inlines = [EventInline]

    @admin.display(description="Название")
    def name(self, obj):
        return obj.event.first().name

    @admin.display(description="Начало")
    def datetime_start(self, obj):
        return obj.event.first().datetime_start

    @admin.display(description="Конец")
    def datetime_end(self, obj):
        return obj.event.first().datetime_end

    @admin.display(description="Место проведения")
    def place(self, obj):
        return obj.event.first().place.name

    def save_formset(self, request, form, formset, change):
        """
        Given an inline formset save it to the database.
        """
        for form in formset.extra_forms:
            form.instance.organizer_id = request.user.id
        formset.save()

    def get_inline_instances(self, request, obj=None):
        inline_instances = []

        for inline_class in self.get_inlines(request, obj):
            inline = inline_class(self.model, self.admin_site)
            if request:
                if not (inline.has_view_or_change_permission(request, obj)):
                    continue
                inline.min_num = 1
                inline.max_num = 1
            inline_instances.append(inline)

        return inline_instances
