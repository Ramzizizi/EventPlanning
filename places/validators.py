from django.core.exceptions import ValidationError


def positive_integer_validator(positive_int: int):
    if positive_int < 0:
        raise ValidationError("Number can't be small zero")
