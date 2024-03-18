from copy import deepcopy

from django.test import TestCase

from events_type import models as event_type_models


class EventDRFViewTest(TestCase):
    password = "admin"
    email = "admin@test.com"

    fixtures = ["fixture.json"]

    create_data_meeting = {
        "name": "Тестовое собрание",
        "place": 1,
        "event_type": 1,
        "event_type_data": {
            "need_visit": True,
            "meeting_theme": "Тестовое выступление",
        },
        "event_capacity": 1,
        "datetime_start": "2024-12-12 14:00:00",
        "datetime_end": "2024-12-12 16:00:00",
        "visitors": [
            1,
        ],
    }
    create_data_conf_call = {
        "name": "Тестовый звонок",
        "place": 1,
        "event_type": 2,
        "event_type_data": {
            "call_url": "http://example.com/",
        },
        "event_capacity": 1,
        "datetime_start": "2024-12-12 14:00:00",
        "datetime_end": "2024-12-12 16:00:00",
        "visitors": [
            1,
        ],
    }
    create_data_conference = {
        "name": "Тестовая конференция",
        "place": 1,
        "event_type": 3,
        "event_type_data": {
            "themes": [
                {
                    "speaker": 1,
                    "theme": "Выступление №1",
                },
                {
                    "speaker": 1,
                    "theme": "Выступление №2",
                },
            ],
        },
        "event_capacity": 1,
        "datetime_start": "2024-12-12 14:00:00",
        "datetime_end": "2024-12-12 16:00:00",
        "visitors": [
            1,
        ],
    }

    def _login(self):
        login_data = {"email": self.email, "password": self.password}
        auth_req = self.client.post("/api/token/", data=login_data)
        return auth_req.data["access"]

    # ==================== EVENTS READ TESTS ====================

    def test_read_all_events_correct(self):
        response = self.client.get("/api/events/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_read_all_events_correct_token(self):
        response = self.client.get(
            "/api/events/",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_read_all_events_incorrect_token(self):
        response = self.client.get(
            "/api/events/",
            HTTP_AUTHORIZATION=f"Bearer 1",
        )

        self.assertEqual(response.status_code, 401)

    # ==================== MEETING TESTS ====================

    def test_post_event_meeting_correct(self):
        create_data = deepcopy(self.create_data_meeting)
        response = self.client.post(
            "/api/events/",
            data=create_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        del response.data["id"]
        del response.data["event_type"]
        create_data.update(
            {
                "organizer": 1,
            },
        )
        del create_data["event_type"]
        del create_data["event_type_data"]

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, create_data)

    def test_post_event_meeting_incorrect_data(self):
        create_data = deepcopy(self.create_data_meeting)
        create_data.update(
            {
                "event_type": 5,
            },
        )
        response = self.client.post(
            "/api/events/",
            data=create_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        self.assertEqual(response.status_code, 400)

    def test_post_event_meeting_incorrect_token(self):
        create_data = deepcopy(self.create_data_meeting)
        response = self.client.post(
            "/api/events/",
            data=create_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer 1",
        )

        self.assertEqual(response.status_code, 401)

    def test_delete_event_meeting_correct(self):
        event_id = event_type_models.Meeting.objects.first().pk
        response = self.client.delete(
            f"/api/events/{event_id}/",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        self.assertEqual(response.status_code, 204)

    def test_delete_event_meeting_incorrect_id(self):
        event_id = 1000
        response = self.client.delete(
            f"/api/events/{event_id}/",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_event_meeting_incorrect_token(self):
        event_id = event_type_models.Meeting.objects.first().pk
        response = self.client.delete(
            f"/api/events/{event_id}/",
            HTTP_AUTHORIZATION="Bearer 1",
        )

        self.assertEqual(response.status_code, 401)

    # ==================== CONF CALL TESTS ====================

    def test_post_event_conf_call_correct(self):
        create_data = deepcopy(self.create_data_conf_call)
        response = self.client.post(
            "/api/events/",
            data=create_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        del response.data["id"]
        del response.data["event_type"]
        create_data.update(
            {
                "organizer": 1,
            },
        )
        del create_data["event_type"]
        del create_data["event_type_data"]

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, create_data)

    def test_post_event_conf_call_incorrect_data(self):
        create_data = deepcopy(self.create_data_conf_call)
        create_data.update(
            {
                "event_type": 5,
            },
        )
        response = self.client.post(
            "/api/events/",
            data=create_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        self.assertEqual(response.status_code, 400)

    def test_post_event_conf_call_incorrect_token(self):
        create_data = deepcopy(self.create_data_conf_call)
        response = self.client.post(
            "/api/events/",
            data=create_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer 1",
        )

        self.assertEqual(response.status_code, 401)

    def test_delete_event_conf_call_correct(self):
        event_id = event_type_models.ConfCall.objects.first().pk
        response = self.client.delete(
            f"/api/events/{event_id}/",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        self.assertEqual(response.status_code, 204)

    def test_delete_event_conf_call_incorrect_id(self):
        event_id = 1000
        response = self.client.delete(
            f"/api/events/{event_id}/",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_event_conf_call_incorrect_token(self):
        event_id = event_type_models.ConfCall.objects.first().pk
        response = self.client.delete(
            f"/api/events/{event_id}/",
            HTTP_AUTHORIZATION="Bearer 1",
        )

        self.assertEqual(response.status_code, 401)

    # ==================== CONFERENCE TESTS ====================

    def test_post_event_conference_correct(self):
        create_data = deepcopy(self.create_data_conference)
        response = self.client.post(
            "/api/events/",
            data=create_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        del response.data["id"]
        del response.data["event_type"]
        create_data.update(
            {
                "organizer": 1,
            },
        )
        del create_data["event_type"]
        del create_data["event_type_data"]

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, create_data)

    def test_post_event_conference_incorrect_data(self):
        create_data = deepcopy(self.create_data_conference)
        create_data.update(
            {
                "event_type": 5,
            },
        )
        response = self.client.post(
            "/api/events/",
            data=create_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        self.assertEqual(response.status_code, 400)

    def test_post_event_conference_incorrect_token(self):
        create_data = deepcopy(self.create_data_conference)
        response = self.client.post(
            "/api/events/",
            data=create_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer 1",
        )

        self.assertEqual(response.status_code, 401)

    def test_delete_event_conference_correct(self):
        event_id = event_type_models.Conference.objects.first().pk
        response = self.client.delete(
            f"/api/events/{event_id}/",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        self.assertEqual(response.status_code, 204)

    def test_delete_event_conference_incorrect_id(self):
        event_id = 1000
        response = self.client.delete(
            f"/api/events/{event_id}/",
            HTTP_AUTHORIZATION=f"Bearer {self._login()}",
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_event_conference_incorrect_token(self):
        event_id = event_type_models.Conference.objects.first().pk
        response = self.client.delete(
            f"/api/events/{event_id}/",
            HTTP_AUTHORIZATION="Bearer 1",
        )

        self.assertEqual(response.status_code, 401)
