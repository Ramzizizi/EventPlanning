from django import forms

from events import models as model_events
from places import models as model_places


class CreateEvent(forms.ModelForm):
    """
    Форма создания мероприятия
    """

    def __init__(self, *args, **kwargs):
        super(CreateEvent, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "form-control", "style": "width: 25%"}
            )

        self.fields["place"].widget.attrs.update({"class": "form-select"})

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
        fields = [
            "name",
            "event_capacity",
            "datetime_start",
            "datetime_end",
            "place",
        ]
        # неиспользуемые поля
        exclude = ["msg_distribute"]
