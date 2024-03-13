from django.urls import path
from events import views as view_events

event_list = view_events.EventViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    },
)

event_detail = view_events.EventViewSet.as_view(
    {
        "get": "retrieve",
        "patch": "partial_update",
        "delete": "destroy",
    },
)
visitors_detail = view_events.EventViewSet.as_view(
    {
        "post": "sign_in",
        "delete": "sign_out",
    },
)

# установка рутов для приложения
urlpatterns = [
    path("", view_events.Event.events_list, name="main"),
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
    path(
        "event_create/",
        view_events.Event.as_view(),
        name="event_create",
    ),
    path("api/events/", event_list),
    path("api/events/<int:pk>/", event_detail),
    path("api/events/<int:pk>/visitor/", visitors_detail),
]
