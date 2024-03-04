from django.contrib import admin

from events import models as event_models
from events_type import models as event_type_models


class EventInline(admin.StackedInline):
    """
    Класс inline для ивента
    """

    model = event_models.Event

    def has_delete_permission(self, request, obj=None):
        """
        Функция проверки прав на удаление
        """
        # при создании типа ивента нельзя удалять сам ивент
        return False


class ThemeInline(admin.StackedInline):
    """
    Класс inline для темы конференции
    """

    model = event_type_models.Themes

    extra = 1


@admin.register(
    event_type_models.Meeting,
    event_type_models.ConfCall,
)
class EventTypeAdmin(admin.ModelAdmin):
    """
    Класс страницы администратора для собраний и конф-звонков
    """

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
        for form in formset.extra_forms:
            form.instance.organizer_id = request.user.id
        formset.save()

    def get_inline_instances(self, request, obj=None):
        """
        Функция настройки отображения inline объектов
        """
        inline_instances = []

        for inline_class in self.get_inlines(request, obj):
            inline = inline_class(self.model, self.admin_site)
            if request:
                if not (inline.has_view_or_change_permission(request, obj)):
                    continue
                # настройка количества объектов для ивентов
                inline.min_num = 1
                inline.max_num = 1
            inline_instances.append(inline)

        return inline_instances


@admin.register(event_type_models.Conference)
class ConferenceAdmin(EventTypeAdmin):
    """
    Класс страницы администратора для конференций
    """

    inlines = [ThemeInline, EventInline]

    def get_inline_instances(self, request, obj=None):
        """
        Функция настройки отображения inline объектов
        """
        inline_instances = []

        for inline_class in self.get_inlines(request, obj):
            inline = inline_class(self.model, self.admin_site)
            if request:
                if not (inline.has_view_or_change_permission(request, obj)):
                    continue
                # настройка количества объектов для ивентов
                if isinstance(inline, EventInline):
                    inline.min_num = 1
                    inline.max_num = 1
                # если объект создан, то нельзя добавлять новые inline
                # сделано для inline тем
                if obj is not None:
                    inline.min_num = 0
                    inline.max_num = 0
            inline_instances.append(inline)

        return inline_instances
