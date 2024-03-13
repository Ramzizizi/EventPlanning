from datetime import datetime

from django.utils.timezone import localtime
from django.core.exceptions import ValidationError


def datetime_type_validator(datetime_value: datetime):
    if not isinstance(datetime_value, datetime):
        raise ValidationError("Start or end is not correct datetime")


def datetime_pass_validator(datetime_value: datetime):
    if datetime_value < localtime():
        raise ValidationError(
            "Event start can't be older than the current date and time",
        )
