from django.test import TestCase

from places import models as place_models


class PlacesViewTest(TestCase):
    password = "admin"
    email = "admin@test.com"

    fixtures = ["fixture.json"]

    def _login(self):
        login_data = {"email": self.email, "password": self.password}
        auth_req = self.client.post("/api/token/", data=login_data)
        return auth_req.data["access"]

    # ==================== PLACES TESTS ====================

    def test_view_drf_read_all_places_correct(self):
        response = self.client.get("/api/places/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_view_drf_read_all_places_incorrect_token(self):
        response = self.client.get(
            "/api/places/",
            HTTP_AUTHORIZATION="Bearer 1",
        )

        self.assertEqual(response.status_code, 401)

    def test_view_drf_read_all_places_correct_token(self):
        response = self.client.get(
            "/api/places/",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    # ==================== ROOMS TESTS ====================

    def test_view_drf_read_all_rooms_correct(self):
        response = self.client.get("/api/places/rooms/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_view_drf_read_all_rooms_correct_token(self):
        response = self.client.get(
            "/api/places/rooms/",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_view_drf_read_all_rooms_incorrect_token(self):
        response = self.client.get(
            "/api/places/rooms/",
            HTTP_AUTHORIZATION="Bearer 1",
        )

        self.assertEqual(response.status_code, 401)

    def test_view_drf_post_room_correct_incomplete_data(self):
        create_data = {"name": "Тестовая комната"}
        correct_response = {
            "name": "Тестовая комната",
            "sofa_count": 0,
            "seat_count": 0,
            "seat_capacity": 0,
            "is_active": True,
        }
        response = self.client.post(
            "/api/places/rooms/",
            data=create_data,
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )
        response.data.pop("id")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, correct_response)

    def test_view_drf_post_room_correct_full_data(self):
        create_data = {
            "name": "Тестовая комната",
            "sofa_count": 2,
            "seat_count": 6,
            "seat_capacity": 10,
            "is_active": 1,
        }
        response = self.client.post(
            "/api/places/rooms/",
            data=create_data,
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )
        response.data.pop("id")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, create_data)

    def test_view_drf_post_room_incorrect_data(self):
        create_data = {
            "name": "Тестовая комната",
            "sofa_count": 2,
            "seat_count": 6,
            "seat_capacity": -10,
            "is_active": 3,
        }
        response = self.client.post(
            "/api/places/rooms/",
            data=create_data,
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        self.assertEqual(response.status_code, 400)

    def test_view_drf_post_room_incorrect_token(self):
        create_data = {"name": "Тестовая комната"}
        response = self.client.post(
            "/api/places/rooms/",
            data=create_data,
            HTTP_AUTHORIZATION="Bearer 1",
        )

        self.assertEqual(response.status_code, 401)

    def test_view_drf_patch_room_correct(self):
        room_id = place_models.Room.objects.first().pk
        patch_data = {"is_active": False}
        response = self.client.patch(
            f"/api/places/rooms/{room_id}/",
            data=patch_data,
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["is_active"], patch_data["is_active"])

    def test_view_drf_patch_room_incorrect_data(self):
        room_id = place_models.Room.objects.first().pk
        patch_data = {"seat_count": -5}
        response = self.client.patch(
            f"/api/places/rooms/{room_id}/",
            data=patch_data,
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_view_drf_patch_room_incorrect_token(self):
        room_id = place_models.Room.objects.first().pk
        patch_data = {"name": "Новое имя комнаты"}
        response = self.client.patch(
            f"/api/places/rooms/{room_id}/",
            data=patch_data,
            HTTP_AUTHORIZATION="Bearer 1",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)

    def test_view_drf_delete_room_correct(self):
        room_id = place_models.Room.objects.first().pk
        response = self.client.delete(
            f"/api/places/rooms/{room_id}/",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        self.assertEqual(response.status_code, 204)

    def test_view_drf_delete_room_incorrect_id(self):
        room_id = place_models.Auditorium.objects.first().pk
        response = self.client.delete(
            f"/api/places/rooms/{room_id}/",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        self.assertEqual(response.status_code, 404)

    def test_view_drf_delete_room_incorrect_token(self):
        room_id = place_models.Room.objects.first().pk
        response = self.client.delete(
            f"/api/places/rooms/{room_id}/",
            HTTP_AUTHORIZATION=f"Bearer 1",
        )

        self.assertEqual(response.status_code, 401)

    # ==================== AUDITORIUMS TESTS ====================

    def test_view_drf_read_all_auditoriums_correct(self):
        response = self.client.get("/api/places/auditoriums/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_view_drf_read_all_auditoriums_correct_token(self):
        response = self.client.get(
            "/api/places/auditoriums/",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_view_drf_read_all_auditoriums_incorrect_token(self):
        response = self.client.get(
            "/api/places/auditoriums/",
            HTTP_AUTHORIZATION="Bearer 1",
        )

        self.assertEqual(response.status_code, 401)

    def test_view_drf_post_auditorium_correct_incomplete_data(self):
        create_data = {"name": "Тестовая аудитория"}
        correct_response = {
            "name": "Тестовая аудитория",
            "mico_count": 0,
            "projects_count": 0,
            "entrances_count": 0,
            "seat_capacity": 0,
            "is_active": True,
        }
        response = self.client.post(
            "/api/places/auditoriums/",
            data=create_data,
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )
        response.data.pop("id")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data, correct_response)

    def test_view_drf_post_auditorium_correct_full_data(self):
        create_data = {
            "name": "Тестовая аудитория",
            "mico_count": 2,
            "projects_count": 1,
            "entrances_count": 2,
            "seat_capacity": 50,
            "is_active": 0,
        }
        response = self.client.post(
            "/api/places/auditoriums/",
            data=create_data,
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )
        response.data.pop("id")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, create_data)

    def test_view_drf_post_auditorium_incorrect_data(
        self,
    ):
        create_data = {
            "name": "Тестовая аудитория",
            "mico_count": 2,
            "projects_count": 1,
            "entrances_count": 2,
            "seat_capacity": -50,
            "is_active": 4,
        }
        response = self.client.post(
            "/api/places/auditoriums/",
            data=create_data,
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )
        self.assertEqual(response.status_code, 400)

    def test_view_drf_post_auditorium_incorrect_token(self):
        create_data = {"name": "Тестовая аудитория"}
        response = self.client.post(
            "/api/places/auditoriums/",
            data=create_data,
            HTTP_AUTHORIZATION="Bearer 1",
        )
        self.assertEqual(response.status_code, 401)

    def test_view_drf_patch_auditorium_correct(self):
        auditorium_id = place_models.Auditorium.objects.first().pk
        patch_data = {"is_active": False}
        response = self.client.patch(
            f"/api/places/auditoriums/{auditorium_id}/",
            data=patch_data,
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["is_active"], patch_data["is_active"])

    def test_view_drf_patch_auditorium_incorrect_data(self):
        auditorium_id = place_models.Auditorium.objects.first().pk
        patch_data = {"seat_capacity": -5}
        response = self.client.patch(
            f"/api/places/auditoriums/{auditorium_id}/",
            data=patch_data,
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_view_drf_patch_auditorium_incorrect_token(self):
        auditorium_id = place_models.Auditorium.objects.first().pk
        patch_data = {"name": "Новое имя аудитории"}
        response = self.client.patch(
            f"/api/places/auditoriums/{auditorium_id}/",
            data=patch_data,
            HTTP_AUTHORIZATION="Bearer 1",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)

    def test_view_drf_delete_auditorium_correct(self):
        auditorium_id = place_models.Auditorium.objects.first().pk
        response = self.client.delete(
            f"/api/places/auditorium/{auditorium_id}/",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        self.assertEqual(response.status_code, 204)

    def test_view_drf_delete_auditorium_incorrect_id(self):
        auditorium_id = place_models.Room.objects.first().pk
        response = self.client.delete(
            f"/api/places/auditorium/{auditorium_id}/",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        self.assertEqual(response.status_code, 404)

    def test_view_drf_delete_auditorium_incorrect_token(self):
        auditorium_id = place_models.Auditorium.objects.first().pk
        response = self.client.delete(
            f"/api/places/auditorium/{auditorium_id}/",
            HTTP_AUTHORIZATION=f"Bearer 1",
        )

        self.assertEqual(response.status_code, 401)
