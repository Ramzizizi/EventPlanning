from django import forms

from events import models as model_events


class CreateEvent(forms.ModelForm):
    """
    Форма создания мероприятия
    """
    class Meta:
        """
        Класс мета-данных
        """
        # модель основания
        model = model_events.Event
        # используемые поля
        fields = ["name", "event_capacity", "start", "end", "place"]
        # неиспользуемые поля
        exclude = ["msg_distribute"]
