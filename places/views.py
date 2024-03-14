from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from places import models as place_models
from places import serializers as place_serializers


class PlaceListViewSet(viewsets.ViewSet, viewsets.generics.ListAPIView):
    queryset = place_models.Place.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = place_serializers.PlaceList

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        for place in queryset:
            place.place_type = (
                "room" if hasattr(place, "room") else "auditorium"
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PlaceViewSet(viewsets.ModelViewSet):
    list_serializers = {
        "create": {
            "rooms": place_serializers.RoomCreate,
            "auditoriums": place_serializers.AuditoriumCreate,
        },
        "list": {
            "rooms": place_serializers.RoomList,
            "auditoriums": place_serializers.AuditoriumList,
        },
        "retrieve": {
            "rooms": place_serializers.RoomBase,
            "auditoriums": place_serializers.AuditoriumBase,
        },
        "partial_update": {
            "rooms": place_serializers.RoomPatch,
            "auditoriums": place_serializers.AuditoriumPatch,
        },
    }
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        return self.list_serializers.get(self.action, {}).get(
            self.kwargs["place_type"],
            {},
        )

    def get_queryset(self):
        if self.kwargs["place_type"] == "rooms":
            return place_models.Room.objects.all()
        return place_models.Auditorium.objects.all()
