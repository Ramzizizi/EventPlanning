from places import views as place_views


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


