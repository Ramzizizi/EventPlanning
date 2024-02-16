from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.req_login, name="login"),
    path("logout/", views.req_logout, name="logout"),
    path("", views.events_list),
    path("event_sign/<int:event_id>", views.event_sign, name="event_sign"),
    path("event_out/<int:event_id>", views.event_out, name="event_out"),
    path("event_create/room/", views.create_event, name="room"),
    path("event_create/meeting_room/", views.create_event, name="meeting_room"),
    path("choice_room/", views.choice_room, name="choice_room"),
]
