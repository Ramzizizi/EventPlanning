from django.core.handlers.wsgi import WSGIRequest
from django import forms
from django.shortcuts import redirect, render
from django.utils.timezone import localtime
from django.views import View
from django.db import transaction

from events import models as event_models
from events import forms as event_forms
from events_type import models as event_type_models
from events_type import views as event_type_views
from events_type import forms as event_type_forms


class Event(View):
    """
    Класс представления для ивентов
    """

    # инициализация форм
    event_create_form = event_forms.CreateEvent
    event_type = event_type_views.EventType()

    @staticmethod
    def event_sign(request: WSGIRequest, event_id: int):
        """
        Функция записи на ивент
        """
        # получение ивента
        event = event_models.Event.event_object.get(pk=event_id)
        # добавление посетителя
        event.visitors.add(request.user)
        # перенаправление на главную страницу
        return redirect("/events/")

    @staticmethod
    def event_out(request: WSGIRequest, event_id: int):
        """
        Функция выхода с ивента
        """
        # получение ивента
        event = event_models.Event.event_object.get(pk=event_id)
        # удаление посетителя
        event.visitors.remove(request.user)
        # перенаправление на главную страницу
        return redirect("/events/")

    @staticmethod
    def events_list(request: WSGIRequest):
        """
        Функция получения ивентов по дате и времени
        """
        # получение временных парамтером
        date_from = request.GET.get("date_from", False)
        date_to = request.GET.get("date_to", False)
        # получение ивентов с ограничением по времени начала
        events = event_models.Event.event_object.filter(
            datetime_start__date__gte=(
                date_from if date_from else localtime().date()
            ),
        )
        # ограничением по времени конца
        if date_to:
            events = events.filter(datetime_end__date__lte=date_to)
        # сортировка по возрастанию начала
        events = events.order_by("datetime_start")
        # заготовка для результата
        available_events, pass_event = [], []
        # сортировка мероприятий по их типу
        for event in events:
            if event.event_status == event_models.EventStatus.PASSED:
                pass_event.append(event)
            else:
                available_events.append(event)
        # рендер страницы с данными
        return render(
            request,
            "base.html",
            {
                "pass_events": pass_event[:5],
                "available_events": available_events,
            },
        )

    def get(self, request: WSGIRequest):
        """
        Функция рендера страницы создания
        """
        return render(
            request,
            "create_event.html",
            {
                "event_create_form": self.event_create_form(),
                "meeting_form": self.event_type.meeting_form(
                    use_required_attribute=False,
                ),
                "conference_form": self.event_type.conference_theme_form(
                    use_required_attribute=False,
                ),
                "conf_call_form": self.event_type.conf_call_form(
                    use_required_attribute=False,
                ),
            },
        )

    @staticmethod
    def _is_form_creation_valid(type_form) -> bool:
        """
        Функция проверки валидности форм
        """

        if not isinstance(type_form, list):
            return type_form.is_valid()

        for theme in type_form:
            if not theme.is_valid():
                return False

        return True

    @staticmethod
    def create_themes(type_form: list[event_type_forms.CreateThemeConference]):
        # создание объектов модели тем конференции
        event_themes = [form.save(commit=False) for form in type_form]
        # создание объекта модели конференции
        event_type = event_type_models.Conference.objects.create()
        # сохранение объекта модели
        event_type.save()

        for theme in event_themes:
            # установка темам id ивента
            theme.event_id = event_type.pk
            # сохранение объектов модели
            theme.save()

        return event_type

    @staticmethod
    def create_event_simple(type_form: forms.ModelForm):
        """
        Функция создания модели из формы
        """
        # создание объекта модели
        event_type = type_form.save(commit=False)
        # сохранение объекта модели
        event_type.save()
        return event_type

    @transaction.atomic
    def post(self, request: WSGIRequest):
        """
        Функция обработки создания ивента
        """
        # укладка данных по ивенту в форму
        event_create_form = self.event_create_form(
            request.POST,
            use_required_attribute=False,
        )
        # получения формы
        type_form = self.event_type.event_type_form_create(request)
        # валидация форм
        if event_create_form.is_valid() and self._is_form_creation_valid(type_form):
            # создание объекта ивента
            event: event_models.Event = event_create_form.save(commit=False)
            # установка организатора
            event.organizer = request.user
            # выбор функции обработки формы
            processor_form = (
                self.create_themes
                if isinstance(type_form, list)
                else self.create_event_simple
            )
            # создание модели из формы
            event_type = processor_form(type_form)
            # установка типа ивента
            event.event_type = event_type
            # сохранение объекта модели
            event.save()
            # возвращение на главную страницу
            return redirect("/events/")

        # рендер страницы создания ивента
        return render(
            request,
            "create_event.html",
            {
                "event_create_form": event_create_form,
                "meeting_form": self.event_type.meeting_form(
                    request.POST,
                    use_required_attribute=False,
                ),
                "conference_form": self.event_type.conference_theme_form(
                    request.POST,
                    use_required_attribute=False,
                ),
                "conf_call_form": self.event_type.conf_call_form(
                    request.POST,
                    use_required_attribute=False,
                ),
            },
        )
