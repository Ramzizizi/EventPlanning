from datetime import datetime

import pytest
from django.core.management import call_command

from events import forms as event_form
from events import models as event_models
from places import models as place_models


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "fixture.json")


@pytest.mark.django_db
def test_event_form_correct():
    place = place_models.Room.objects.first()
    form = event_form.CreateEvent(
        {
            "name": "Тестовое мероприятие",
            "event_capacity": 2,
            "datetime_start": datetime(2026, 12, 12, 12),
            "datetime_end": datetime(2026, 12, 12, 14),
            "place": place.pk,
        }
    )
    form_valid_status = form.is_valid()
    assert form_valid_status


@pytest.mark.django_db
def test_event_form_incorrect_time():
    place = place_models.Room.objects.first()
    form = event_form.CreateEvent(
        {
            "name": "Тестовое мероприятие",
            "event_capacity": 2,
            "datetime_start": datetime(2000, 12, 12, 12),
            "datetime_end": datetime(2000, 12, 12, 14),
            "place": place.pk,
        }
    )
    form_valid_status = form.is_valid()
    assert not form_valid_status


@pytest.mark.django_db
def test_event_form_incorrect_data():
    with pytest.raises(event_models.Event.place.RelatedObjectDoesNotExist):
        form = event_form.CreateEvent(
            {
                "name": "Тестовое мероприятие",
                "event_capacity": 2,
                "datetime_start": datetime(2026, 12, 12, 12),
                "datetime_end": datetime(2026, 12, 12, 14),
                "place": 1000,
            }
        )
        form.is_valid()


@pytest.mark.django_db
def test_event_form_incorrect_capacity():
    with pytest.raises(ValueError):
        place = place_models.Room.objects.first()
        form = event_form.CreateEvent(
            {
                "name": "Тестовое мероприятие",
                "event_capacity": 2000,
                "datetime_start": datetime(2026, 12, 12, 12),
                "datetime_end": datetime(2026, 12, 12, 14),
                "place": place.pk,
            }
        )
        form.is_valid()
        form.save(commit=False)
