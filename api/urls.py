from django.urls import path
from rest_framework_simplejwt import views

from places import views as place_views
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
base_places_list = place_views.PlaceListViewSet.as_view(
    {
        "get": "list",
    },
)

places_list = place_views.PlaceViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

places_detail = place_views.PlaceViewSet.as_view(
    {
        "get": "retrieve",
        "patch": "partial_update",
        "delete": "destroy",
    },
)

urlpatterns = [
    path("events/", event_list),
    path("events/<int:pk>/", event_detail),
    path("events/<int:pk>/visitor/", visitors_detail),
    path("places/", base_places_list),
    path("places/<str:place_type>/", places_list),
    path("places/<str:place_type>/<int:pk>/", places_detail),
    path(
        "token/",
        views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
