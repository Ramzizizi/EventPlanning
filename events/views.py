from typing import Iterable
from itertools import islice

from django.core.handlers.wsgi import WSGIRequest
from django.forms import modelformset_factory, modelform_factory
from django.shortcuts import redirect, render
from django.utils.timezone import localtime
from django.views import View
from django.db import transaction

from users import models as user_models
from events import models as event_models
from events import forms as event_forms
from events_type import forms as event_type_forms
from events_type import models as event_type_models


class Event(View):
    """
    Класс представления для ивентов
    """

    # инициализация форм
    event_create_form = event_forms.CreateEvent
    meeting_form = event_type_forms.CreateMeeting
    conf_call_form = event_type_forms.CreateConfCall
    conference_theme_form = event_type_forms.CreateThemeConference

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
                "meeting_form": self.meeting_form(use_required_attribute=False),
                "conference_form": self.conference_theme_form(
                    use_required_attribute=False,
                ),
                "conf_call_form": self.conf_call_form(
                    use_required_attribute=False,
                ),
            },
        )

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
        # получения типа ивента
        type_form = self.event_type_form_create(request)
        if event_create_form.is_valid() and (
            type_form.is_valid()
            if not isinstance(
                type_form,
                list,
            )
            else [theme.is_valid() for theme in type_form]
        ):
            # создание объекта ивента
            event: event_models.Event = event_create_form.save(commit=False)
            # установка организатора
            event.organizer = request.user
            # если объект лист, то это набор тем для конференции
            if isinstance(type_form, list):
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
            else:
                # создание объекта модели
                event_type = type_form.save(commit=False)
                # сохранение объекта модели
                event_type.save()
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
                "meeting_form": self.meeting_form(
                    request.POST,
                    use_required_attribute=False,
                ),
                "conference_form": self.conference_theme_form(
                    request.POST,
                    use_required_attribute=False,
                ),
                "conf_call_form": self.conf_call_form(
                    request.POST,
                    use_required_attribute=False,
                ),
            },
        )

    def event_type_form_create(self, request: WSGIRequest):
        """
        Функция укладки в форму типа ивента
        """
        # укладка в форму собрания
        type_form = self.create_meeting_from(request)
        # укладка в форму конференц-звонка
        type_form = (
            type_form
            if type_form.changed_data
            else self.create_conf_call_from(request)
        )
        # укладка в форму конференции
        type_form = (
            type_form
            if type_form.changed_data
            else self.create_theme_from(request)
        )
        return type_form

    def create_meeting_from(self, request: WSGIRequest):
        """
        Функция создания формы для собрания

        :return: Форма собрания если есть данные по собранию
        """
        # создание формы
        meeting_form = self.meeting_form(
            request.POST,
            use_required_attribute=False,
        )
        # если данные в форме не пустые, возвращается форма
        if meeting_form.changed_data is not None:
            return meeting_form
        return None

    def create_conf_call_from(self, request: WSGIRequest):
        """
        Функция создания формы для конференц-звонка

        :return: Форма конференц-звонка если есть данные по конференц-звонку
        """
        # создание формы
        conf_call_form = self.conf_call_form(
            request.POST,
            use_required_attribute=False,
        )
        # если данные в форме не пустые, возвращается форма
        if conf_call_form.changed_data is not None:
            return conf_call_form
        return None

    def create_theme_from(self, request: WSGIRequest):
        """
        Функция создания формы для тем конференции

        :return: Лист форм тем конференции
        """
        # преобразование данных
        theme_data = {
            key: value
            for key, value in request.POST.items()
            if ("theme" in key or "speaker" in key) and (key != "meeting_theme")
        }
        # нарезка данных на чанки
        sliced_data = self.conf_chunked(theme_data.values())
        # укладка данных в форму
        forms = [self.conference_theme_form(data) for data in sliced_data]
        # если данные не пустые, возвращает лист форм
        if any(forms):
            return forms
        return None

    @staticmethod
    def conf_chunked(conf_data: Iterable, chunk_size: int = 2):
        """
        Разделение итерируемого объекта на чанки заданного размера
        """
        result = []
        # преобразование объекта в итератор
        iterator = iter(conf_data)
        # цикл по итератору
        while chunk := list(islice(iterator, chunk_size)):
            result.append({"speaker": chunk[0], "theme": chunk[1]})
        return result
