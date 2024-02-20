from django import forms

from events import models as model_events


class CreateEvent(forms.ModelForm):
    class Meta:
        model = model_events.Event
        fields = ["name", "event_capacity", "start", "end", "place"]
        exclude = ["msg_distribute"]
