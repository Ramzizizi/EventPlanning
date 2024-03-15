from django.urls import path

from events import views as event_views


event_list = event_views.EventViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    },
)

event_detail = event_views.EventViewSet.as_view(
    {
        "get": "retrieve",
        "patch": "partial_update",
        "delete": "destroy",
    },
)
visitors_detail = event_views.EventViewSet.as_view(
    {
        "post": "sign_in",
        "delete": "sign_out",
    },
)


# установка рутов для приложения
urlpatterns = [
    path("", event_views.Event.events_list, name="main"),
    path(
        "event_sign/<int:event_id>",
        event_views.Event.event_sign,
        name="event_sign",
    ),
    path(
        "event_out/<int:event_id>",
        event_views.Event.event_out,
        name="event_out",
    ),
    path(
        "event_create/",
        event_views.Event.as_view(),
        name="event_create",
    ),
]
