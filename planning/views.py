from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from . import models
from .forms import CreateEventInRoom, CreateEventInMeetingRoom


def event_sign(request, event_id):
    event = models.Event.objects.get(pk=event_id)
    event.visitors.add(request.user)
    return redirect("/planning/")


def event_out(request, event_id):
    event = models.Event.objects.get(pk=event_id)
    event.visitors.remove(request.user)
    return redirect("/planning/")


def events_list(request):
    upcoming_events = (
        models.Event.objects.exclude(event_status=1).order_by("start").all()
    )
    [event.check_status for event in upcoming_events]
    old_events = models.Event.objects.filter(event_status=1).order_by("start").all()[:5]
    return render(
        request,
        "base.html",
        {"upcoming_events": upcoming_events, "old_events": old_events},
    )


def req_login(request):
    user = authenticate(
        request, username=request.POST["email"], password=request.POST["pass"]
    )
    if user is not None:
        login(request, user)
    return redirect("/planning/")


def req_logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
    return redirect("/planning/")


def create_event(request):
    if request.method == "POST":
        if "meeting_room" in request.path:
            form = CreateEventInMeetingRoom(request.POST)
        else:
            form = CreateEventInRoom(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect("/planning/")
    else:
        if "meeting_room" in request.path:
            form = CreateEventInMeetingRoom()
        else:
            form = CreateEventInRoom()
    return render(request, "create_event.html", context={"form": form})


def choice_room(request):
    rooms = models.Room.objects.all()
    meeting_rooms = models.MeetingRoom.objects.all()
    return render(
        request,
        "room_choose.html",
        context={"rooms": rooms, "meeting_rooms": meeting_rooms},
    )
