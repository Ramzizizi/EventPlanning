from django.db import models
from django.test import TestCase

from places import models as place_models


class PlaceTestCase(TestCase):
    def setUp(self):
        place_models.Room.objects.create(
            seat_capacity=10,
            name="Комната",
            sofa_count=1,
            seat_count=4,
        )
        place_models.Auditorium.objects.create(
            seat_capacity=20,
            name="Аудитория",
            mico_count=1,
            projects_count=1,
            entrances_count=2,
        )

    def test_valid_data_type_fields_place(self):
        place = place_models.Place.objects.first()
        self.assertEqual(
            type(place._meta.get_field("seat_capacity")),
            models.PositiveIntegerField,
        )
        self.assertEqual(
            type(place._meta.get_field("name")),
            models.CharField,
        )
        self.assertEqual(
            type(place._meta.get_field("is_active")),
            models.BooleanField,
        )

    def test_valid_data_type_fields_room(self):
        room = place_models.Room.objects.get(name="Комната")
        self.assertEqual(
            type(room._meta.get_field("sofa_count")),
            models.PositiveIntegerField,
        )
        self.assertEqual(
            type(room._meta.get_field("seat_count")),
            models.PositiveIntegerField,
        )

    def test_valid_data_type_fields_auditorium(self):
        auditorium = place_models.Auditorium.objects.get(name="Аудитория")
        self.assertEqual(
            type(auditorium._meta.get_field("mico_count")),
            models.PositiveIntegerField,
        )
        self.assertEqual(
            type(auditorium._meta.get_field("projects_count")),
            models.PositiveIntegerField,
        )
        self.assertEqual(
            type(auditorium._meta.get_field("entrances_count")),
            models.PositiveIntegerField,
        )

    def test_active_status_check(self):
        room = place_models.Room.objects.get(name="Комната")
        auditorium = place_models.Auditorium.objects.get(name="Аудитория")

        self.assertTrue(room.is_active)
        self.assertTrue(auditorium.is_active)

        room.is_active = False
        auditorium.is_active = False

        self.assertFalse(room.is_active)
        self.assertFalse(auditorium.is_active)

    def test_active_manager(self):
        rooms = place_models.Room.active_places.all()

        self.assertEqual(len(rooms), 1)

        for room in rooms:
            room.is_active = False
            room.save()

        active_rooms = place_models.Room.active_places.all()
        all_rooms = place_models.Room.objects.all()

        self.assertEqual(len(active_rooms), 0)
        self.assertEqual(len(all_rooms), 1)
