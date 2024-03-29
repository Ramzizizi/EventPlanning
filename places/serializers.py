from rest_framework import serializers

from places import models as place_models
from places import validators as place_validators


class PlaceBase(serializers.ModelSerializer):
    seat_capacity = serializers.IntegerField(
        default=0,
        required=False,
        validators=[place_validators.positive_integer_validator],
    )
    name = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        required=True,
    )
    is_active = serializers.BooleanField(
        default=True,
        required=False,
    )

    class Meta:
        model = place_models.Place
        fields = "__all__"


class PlaceList(PlaceBase):
    place_type = serializers.CharField(
        read_only=True,
        required=False,
    )


class RoomBase(PlaceBase):
    sofa_count = serializers.IntegerField(
        default=0,
        required=False,
        validators=[place_validators.positive_integer_validator],
    )
    seat_count = serializers.IntegerField(
        default=0,
        required=False,
        validators=[place_validators.positive_integer_validator],
    )

    class Meta:
        model = place_models.Room
        fields = "__all__"


class RoomCreate(RoomBase):
    ...


class RoomPatch(RoomBase):
    ...


class RoomList(RoomBase):
    ...


class AuditoriumBase(PlaceBase):
    mico_count = serializers.IntegerField(
        default=0,
        required=False,
        validators=[place_validators.positive_integer_validator],
    )
    projects_count = serializers.IntegerField(
        default=0,
        required=False,
        validators=[place_validators.positive_integer_validator],
    )
    entrances_count = serializers.IntegerField(
        default=0,
        required=False,
        validators=[place_validators.positive_integer_validator],
    )

    class Meta:
        model = place_models.Auditorium
        fields = "__all__"


class AuditoriumCreate(AuditoriumBase):
    ...


class AuditoriumPatch(AuditoriumBase):
    ...


class AuditoriumList(AuditoriumBase):
    ...
