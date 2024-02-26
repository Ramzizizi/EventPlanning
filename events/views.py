from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, render
from django.utils.timezone import localtime
from django.views import View

from events import models as model_events
from events import forms as form_events


class Event(View):

    form = form_events.CreateEvent

    @staticmethod
    def event_sign(request, event_id):
        event = model_events.Event.event_object.get(pk=event_id)
        event.visitors.add(request.user)
        return redirect("/events/")

    @staticmethod
    def event_out(request, event_id):
        event = model_events.Event.event_object.get(pk=event_id)
        event.visitors.remove(request.user)
        return redirect("/events/")

    @staticmethod
    def events_list(request):
        events = (
            model_events.Event.event_object.filter(
                start__date=localtime().date()
            )
            .order_by("start")
            .all()
        )
        available_events, pass_event = [], []

        for event in events:
            if event.event_status == model_events.EventStatus.PASSED:
                pass_event.append(event)
            else:
                available_events.append(event)

        return render(
            request,
            "base.html",
            {
                "pass_events": pass_event,
                "available_events": available_events,
            },
        )

    def post(self, request: WSGIRequest):
        form = self.form(request.POST)
        if form.is_valid():
            event: model_events.Event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect("/events/")
        return render(request, "create_event.html", {"form": form})

    def get(self, request: WSGIRequest):
        form = self.form()
        return render(request, "create_event.html", {"form": form})
