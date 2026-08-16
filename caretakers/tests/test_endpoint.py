from __future__ import annotations
import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from caretakers.models import Caretaker

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


def make_payload(**overrides) -> dict:
    payload = {
        "full_name": "Micaela Rodriguez",
        "dni": f"{uuid.uuid4().int % 10000000}",
        "email": f"test_{uuid.uuid4().hex[:5]}@gmail.com",
        "phone": "381123456",
        "status": Caretaker.Status.ACTIVE,
    }
    payload.update(overrides)
    return payload


class TestListCaretakers:
    def test_returns_paginated_list(self, api_client: APIClient) -> None:
        Caretaker.objects.create(**{**make_payload(), "full_name": "A"})
        Caretaker.objects.create(**{**make_payload(), "full_name": "B"})

        response = api_client.get("/api/caretakers/")
        print(response)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

    def test_filters_by_status(self, api_client: APIClient) -> None:
        Caretaker.objects.create(**{**make_payload(), "status": Caretaker.Status.BLOCKED})

        Caretaker.objects.create(**{**make_payload(), "status": Caretaker.Status.ACTIVE})

        response = api_client.get("/api/caretakers/", {"status": Caretaker.Status.ACTIVE})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["status"] == "active"


class TestRetrieveCaretaker:
    def test_returns_caretaker_detail(self, api_client: APIClient) -> None:
        caretaker = Caretaker.objects.create(**make_payload())

        response = api_client.get(f"/api/caretakers/{caretaker.pk}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == caretaker.pk

    def test_returns_404_when_not_found(self, api_client: APIClient) -> None:
        response = api_client.get("/api/caretakers/01ARZ3NDEKTSV4RRFFQ69G5FAV/")

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestCreateCaretaker:
    def test_creates_caretaker_with_valid_payload(self, api_client: APIClient) -> None:
        response = api_client.post("/api/caretakers/", make_payload(), format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["full_name"] == "Micaela Rodriguez"
        assert Caretaker.objects.count() == 1

    def test_returns_400_with_invalid_payload(self, api_client: APIClient) -> None:
        payload = make_payload()
        payload.pop("full_name")

        response = api_client.post("/api/caretakers/", payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestUpdateCaretaker:
    def test_partial_update_modifies_field(self, api_client: APIClient) -> None:
        caretaker = Caretaker.objects.create(**make_payload())

        response = api_client.patch(
            f"/api/caretakers/{caretaker.pk}/",
            {"status": Caretaker.Status.BLOCKED},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        caretaker.refresh_from_db()
        assert caretaker.status == Caretaker.Status.BLOCKED


class TestDeleteCaretaker:
    def test_deletes_existing_caretaker(self, api_client: APIClient) -> None:
        caretaker = Caretaker.objects.create(**make_payload())

        response = api_client.delete(f"/api/caretakers/{caretaker.pk}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Caretaker.objects.filter(pk=caretaker.pk).exists()