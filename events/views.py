from itertools import islice

from django.core.handlers.wsgi import WSGIRequest
from django.forms import modelformset_factory, modelform_factory
from django.shortcuts import redirect, render
from django.utils.timezone import localtime
from django.views import View

from users import models as user_models
from events import models as event_models
from events import forms as event_forms
from events_type import forms as event_type_forms
from events_type import models as event_type_models


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
        events = event_models.Event.event_object.filter(
            datetime_start__date__gte=(
                date_from if date_from else localtime().date()
            )
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

    def get(self, request: WSGIRequest):
        return render(
            request,
            "create_event.html",
            {
                "event_create_form": self.event_create_form(),
                "meeting_form": self.meeting_form(use_required_attribute=False),
                "conference_form": self.conference_form(
                    use_required_attribute=False
                ),
                "conf_call_form": self.conf_call_form(
                    use_required_attribute=False
                ),
            },
        )

    def post(self, request: WSGIRequest):
        event_create_form = self.event_create_form(
            request.POST,
            use_required_attribute=False,
        )
        type_form = self.event_type_form_create(request)
        if event_create_form.is_valid():
            event: event_models.Event = event_create_form.save(commit=False)
            event.organizer = request.user
            if type(type_form) is list:
                event_themes = [form.save(commit=False) for form in type_form]
                event_type = event_type_models.Conference.objects.create()
                event_type.save()
                for theme in event_themes:
                    theme.event_id = event_type.pk
                    theme.save()
            else:
                event_type = type_form.save(commit=False)
                event_type.save()
            event.event_type = event_type
            event.save()
            return redirect("/events/")
        return render(
            request,
            "create_event.html",
            {
                "event_create_form": event_create_form,
                "meeting_form": self.meeting_form(
                    request.POST,
                    use_required_attribute=False,
                ),
                "conference_form": self.conference_form(
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
        type_form = self.create_meeting_from(request)
        type_form = (
            type_form
            if type_form.changed_data
            else self.create_conf_call_from(request)
        )
        type_form = (
            type_form
            if type_form.changed_data
            else self.create_conference_from(request)
        )
        return type_form

    def create_meeting_from(self, request: WSGIRequest):
        meeting_form = self.meeting_form(
            request.POST,
            use_required_attribute=False,
        )
        if meeting_form.changed_data is not None:
            return meeting_form
        return

    def create_conf_call_from(self, request: WSGIRequest):
        conf_call_form = self.conf_call_form(
            request.POST,
            use_required_attribute=False,
        )
        if conf_call_form.changed_data is not None:
            return conf_call_form
        return

    def create_conference_from(self, request: WSGIRequest):
        conf_data = {
            k: v
            for k, v in request.POST.items()
            if ("theme" in k or "speaker" in k) and (k != "meeting_theme")
        }
        sliced_data = self.conf_chunked(conf_data.values())
        forms = [self.conference_form(data) for data in sliced_data]
        if any(forms):
            return forms
        return

    @staticmethod
    def conf_chunked(conf_data):
        result = []
        iterator = iter(conf_data)
        while chunk := list(islice(iterator, 2)):
            result.append({"speaker": chunk[0], "theme": chunk[1]})
        return result
