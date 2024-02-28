from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, render
from django.utils.timezone import localtime
from django.views import View

from users import forms as user_forms
from users import models as user_models
from events import models as event_models
from events import forms as event_forms
from events_type import forms as event_type_forms


class Event(View):

    event_create_form = event_forms.CreateEvent
    meeting_form = event_type_forms.CreateMeeting
    conf_call_form = event_type_forms.CreateConfCall
    conference_form = event_type_forms.CreateConference

    @staticmethod
    def event_sign(request, event_id):
        event = event_models.Event.event_object.get(pk=event_id)
        event.visitors.add(request.user)
        return redirect("/events/")

    @staticmethod
    def event_out(request, event_id):
        event = event_models.Event.event_object.get(pk=event_id)
        event.visitors.remove(request.user)
        return redirect("/events/")

    @staticmethod
    def events_list(request: WSGIRequest):
        date_from = request.GET.get("date_from", False)
        date_to = request.GET.get("date_to", False)
        if date_from:
            events = event_models.Event.event_object.filter(
                datetime_start__date__gte=date_from
            )
        else:
            events = event_models.Event.event_object.filter(
                datetime_start__date__gte=localtime().date()
            )
        if date_to:
            events = events.filter(datetime_end__date__lte=date_to)
        events = events.order_by("datetime_start")

        available_events, pass_event = [], []

        for event in events:
            if event.event_status == event_models.EventStatus.PASSED:
                pass_event.append(event)
            else:
                available_events.append(event)

        return render(
            request,
            "base.html",
            {
                "pass_events": pass_event[:5],
                "available_events": available_events,
            },
        )

    def post(self, request: WSGIRequest):
        event_create_form = self.event_create_form(request.POST)
        meeting_form = self.meeting_form(request.POST)
        conference_form = self.conference_form(request.POST)
        conf_call_form = self.conf_call_form(request.POST)
        if meeting_form.changed_data:
            type_form = meeting_form
        elif conf_call_form.changed_data:
            type_form = conf_call_form
        else:
            type_form = conference_form
        if event_create_form.is_valid() and type_form.is_valid():
            event: event_models.Event = event_create_form.save(commit=False)
            event_type = type_form.save(commit=False)
            event_type.save()
            event.organizer = request.user
            event.event_type = event_type
            event.save()
            return redirect("/events/")
        return render(
            request,
            "create_event.html",
            {
                "event_create_form": event_create_form,
                "meeting_form": meeting_form,
                "conference_form": conference_form,
                "conf_call_form": conf_call_form,
            },
        )

    def get(self, request: WSGIRequest):
        return render(
            request,
            "create_event.html",
            {
                "event_create_form": self.event_create_form(),
                "meeting_form": self.meeting_form(use_required_attribute=False),
                "conference_form": user_forms.SpeakerFormSet(
                    queryset=user_models.Speaker.objects.none()
                ),
                "conf_call_form": self.conf_call_form(
                    use_required_attribute=False
                ),
            },
        )
