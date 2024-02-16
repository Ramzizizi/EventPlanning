from django import forms
from .models import Event, Room, MeetingRoom


class CreateEventInRoom(forms.ModelForm):
    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Место проведения",
    )

    class Meta:
        model = Event
        fields = ["name", "event_capacity", "start", "end", "room"]
        exclude = ["meeting_room"]


class CreateEventInMeetingRoom(forms.ModelForm):
    meeting_room = forms.ModelChoiceField(
        queryset=MeetingRoom.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Место проведения",
    )

    class Meta:
        model = Event
        fields = ["name", "event_capacity", "start", "end", "meeting_room"]
        exclude = ["room"]
