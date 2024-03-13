from itertools import islice
from typing import Iterable

from django.http import Http404
from django.core.handlers.wsgi import WSGIRequest
from django.views import View

from events_type import forms as event_type_forms


class EventBase(View):
    """
    Класс представлений для типов ивентов
    """

    # инициализация форм
    meeting_form = event_type_forms.CreateMeeting
    conf_call_form = event_type_forms.CreateConfCall
    conference_theme_form = event_type_forms.CreateThemeConference

    @property
    def _mapping_processors_form(self):
        """
        Карта функций дял формирования формы

        :return: Одна из трёх функций для формирования формы
        """
        return {
            "meeting": self._create_meeting_form,
            "conf_call": self._create_conf_call_form,
            "conference": self._create_theme_form,
        }

    def _get_processor_form(self, event_type: str):
        """
        Получение функции для формирования формы
        """
        processor = self._mapping_processors_form.get(event_type)
        # при отсутствии формы возвращает ошибку
        if processor is None:
            raise Http404

        return processor

    @staticmethod
    def _conf_chunked(conf_data: Iterable, chunk_size: int):
        """
        Генератор чанков
        """
        # преобразование объекта в итератор
        iterator = iter(conf_data)
        # цикл по итератору
        while chunk := list(islice(iterator, chunk_size)):
            yield {"speaker": chunk[0], "theme": chunk[1]}

    def event_type_form_create(self, request: WSGIRequest):
        """
        Функция укладки в форму типа ивента
        """
        processor = self._get_processor_form(request.POST.get("event_type"))
        return processor(request)

    def _create_meeting_form(self, request: WSGIRequest):
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

    def _create_conf_call_form(self, request: WSGIRequest):
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

    def _create_theme_form(self, request: WSGIRequest):
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
        sliced_data = self._conf_chunked(
            theme_data.values(),
            chunk_size=self.conference_theme_form.Meta.chunk_size,
        )
        # укладка данных в форму
        forms = [self.conference_theme_form(data) for data in sliced_data]
        # если данные не пустые, возвращает лист форм
        if any(forms):
            return forms

        return None
