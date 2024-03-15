from collections import OrderedDict

from django.db.models import Q, Sum, Model
from django.db.models.functions import Coalesce
from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject

from users import models as user_models
from places import models as place_model
from events import models as event_models
from events import validators as event_validators
from events_type import models as event_type_models
from events_type.serializers import event_type_serializers

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class EventShortInfo(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        allow_null=False,
    )
    datetime_start = serializers.DateTimeField(
        format=DATETIME_FORMAT,
        required=True,
        allow_null=False,
        validators=[
            event_validators.datetime_type_validator,
            event_validators.datetime_pass_validator,
        ],
    )
    datetime_end = serializers.DateTimeField(
        format=DATETIME_FORMAT,
        required=True,
        allow_null=False,
        validators=[
            event_validators.datetime_type_validator,
            event_validators.datetime_pass_validator,
        ],
    )

    class Meta:
        model = event_models.Event
        exclude = [
            "organizer",
            "visitors",
            "event_capacity",
            "place",
            "event_type",
            "msg_distribute",
        ]


class EventBase(serializers.ModelSerializer):

    name = serializers.CharField(
        required=True,
        allow_null=False,
    )
    event_capacity = serializers.IntegerField(
        required=True,
        allow_null=False,
    )
    datetime_start = serializers.DateTimeField(
        format=DATETIME_FORMAT,
        required=True,
        allow_null=False,
        validators=[
            event_validators.datetime_type_validator,
            event_validators.datetime_pass_validator,
        ],
    )
    datetime_end = serializers.DateTimeField(
        format=DATETIME_FORMAT,
        required=True,
        allow_null=False,
        validators=[
            event_validators.datetime_type_validator,
            event_validators.datetime_pass_validator,
        ],
    )
    place = serializers.PrimaryKeyRelatedField(
        queryset=place_model.Place.objects,
        many=False,
        required=True,
        allow_null=False,
    )
    event_type = serializers.PrimaryKeyRelatedField(
        queryset=event_type_models.EventBase.objects,
        many=False,
        required=True,
        allow_null=False,
    )
    visitors = serializers.PrimaryKeyRelatedField(
        queryset=user_models.CustomUser.objects,
        many=True,
        allow_empty=True,
    )

    class Meta:
        model = event_models.Event
        exclude = ["msg_distribute"]


class EventPatch(EventBase):

    name = serializers.CharField(
        required=False,
        allow_null=False,
    )
    event_capacity = serializers.IntegerField(
        required=False,
        allow_null=False,
        read_only=True,
    )
    datetime_start = serializers.DateTimeField(
        format=DATETIME_FORMAT,
        required=False,
        allow_null=False,
        validators=[
            event_validators.datetime_type_validator,
            event_validators.datetime_pass_validator,
        ],
        read_only=True,
    )
    datetime_end = serializers.DateTimeField(
        format=DATETIME_FORMAT,
        required=False,
        allow_null=False,
        validators=[
            event_validators.datetime_type_validator,
            event_validators.datetime_pass_validator,
        ],
        read_only=True,
    )
    place = serializers.PrimaryKeyRelatedField(
        many=False,
        required=False,
        allow_null=False,
        read_only=True,
    )
    event_type = serializers.PrimaryKeyRelatedField(
        many=False,
        required=False,
        allow_null=False,
        read_only=True,
    )
    visitors = serializers.PrimaryKeyRelatedField(
        queryset=user_models.CustomUser.objects,
        many=True,
        allow_empty=True,
    )


class EventCreate(EventBase):
    EVENT_TYPE_CHOICES = ((1, "meeting"), (2, "conf_call"), (3, "conference"))

    event_type = serializers.ChoiceField(choices=EVENT_TYPE_CHOICES)
    event_type_data = serializers.JSONField(
        write_only=True,
        required=True,
        allow_null=False,
    )

    def validate(self, attrs):
        # проверка начала и конца ивента
        if not self._is_start_end_valid(**attrs):
            raise serializers.ValidationError(
                {
                    "datetime_end": "Event end can't be newer the he start",
                },
            )
            # проверка на кол-во свободных мест в комнате
        if not self._is_capacity_valid(**attrs):
            raise serializers.ValidationError(
                {
                    "event_capacity": "Event capacity bigger then place capacity",
                },
            )
        if not self._is_event_type_data_valid(**attrs):
            raise serializers.ValidationError(
                {
                    "event_type": "Event type data is not valid",
                },
            )
        return attrs

    @staticmethod
    def _is_start_end_valid(datetime_start, datetime_end, **_):
        return datetime_end >= datetime_start

    @staticmethod
    def _is_capacity_valid(
        place,
        event_capacity,
        datetime_start,
        datetime_end,
        **_,
    ):
        events_capacity = (
            event_models.Event.event_object.filter(
                Q(place__pk=place.pk)
                & (
                    Q(datetime_start__lte=datetime_start)
                    & Q(datetime_end__gte=datetime_start)
                )
                | (
                    Q(datetime_start__lte=datetime_end)
                    & Q(datetime_end__gte=datetime_end)
                ),
            ).aggregate(sum=Coalesce(Sum("event_capacity"), 0))
        )["sum"]
        return (place.seat_capacity - events_capacity) >= event_capacity

    @staticmethod
    def _is_event_type_data_valid(event_type, event_type_data, **_):
        serializer = event_type_serializers[event_type]
        event_type_date = serializer(data=event_type_data)
        return event_type_date.is_valid()

    def to_representation(self, instance):
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            check_for_none = (
                attribute.pk
                if isinstance(attribute, PKOnlyObject)
                else attribute
            )

            if check_for_none is None:
                ret[field.field_name] = None
            else:
                value = (
                    attribute.pk
                    if isinstance(attribute, Model)
                    else field.to_representation(attribute)
                )
                ret[field.field_name] = value

        return ret
