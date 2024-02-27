from django.urls import path

from events import views as view_events

# установка рутов для приложения
urlpatterns = [
    path("", view_events.Event.events_list, name='main'),
    path(
        "event_sign/<int:event_id>",
        view_events.Event.event_sign,
        name="event_sign",
    ),
    path(
        "event_out/<int:event_id>",
        view_events.Event.event_out,
        name="event_out",
    ),
    path("event_create/", view_events.Event.as_view(), name="event_create"),
]
