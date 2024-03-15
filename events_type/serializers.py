import enum

from rest_framework import serializers

from events_type import models as event_type_models


class Theme(serializers.ModelSerializer):
    class Meta:
        # модель основания
        model = event_type_models.Themes
        # используемые поля
        fields = ["speaker", "theme"]
        # количество полей для создания чанка
        chunk_size = len(fields)


class Conference(serializers.Serializer):
    themes = Theme(many=True)


class Meeting(serializers.ModelSerializer):

    class Meta:
        """
        Класс мета-данных
        """

        # модель основания
        model = event_type_models.Meeting
        # используемые поля
        fields = ["need_visit", "meeting_theme"]


class ConfCall(serializers.ModelSerializer):

    class Meta:
        """
        Класс мета-данных
        """

        # модель основания
        model = event_type_models.ConfCall
        # используемые поля
        fields = ["call_url"]


class EventTypes(enum.Enum):
    Meeting = 1
    ConfCall = 2
    Conference = 3


event_type_serializers = {
    EventTypes.Meeting.value: Meeting,
    EventTypes.ConfCall.value: ConfCall,
    EventTypes.Conference.value: Conference,
}
