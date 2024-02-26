from django import forms

from events import models as model_events
from places import models as model_places


class CreateEvent(forms.ModelForm):
    """
    Форма создания мероприятия
    """

    place = forms.ModelChoiceField(
        widget=forms.Select,
        queryset=model_places.Place.active_places.all(),
        label="Место проведения",
    )

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
