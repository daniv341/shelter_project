from __future__ import annotations
import random
import time
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
    """Payload minimo valido para crear un caretaker (todos los campos requeridos)."""
    payload = {
        "full_name": "nombre de prueba",
        "dni": random.randint(1_000_000, 99_999_999),
        "email": f"test_{uuid.uuid4().hex[:5]}@gmail.com",
        "phone": random.randint(100_000, 999_999_999),
        "status": Caretaker.Status.ACTIVE,
    }
    payload.update(overrides)
    return payload


def make_optional_only_payload(**overrides) -> dict:
    """Payload solo con los campos requeridos, sin los opcionales."""
    payload = {
        "full_name": "nombre de prueba",
        "dni": random.randint(1_000_000, 99_999_999),
        "status": Caretaker.Status.ACTIVE,
    }
    payload.update(overrides)
    return payload


@pytest.fixture
def caretaker_payload() -> dict:
    return make_payload()

@pytest.fixture
def caretaker_optional_payload() -> dict:
    return make_optional_only_payload()


@pytest.fixture
def created_caretaker(caretaker_payload, api_client) -> dict:
    response = api_client.post("/api/caretakers/", caretaker_payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED, f"Setup fallo: {response.data}"
    return response.data


class TestCreateCaretaker:
    def test_create_caretaker_success(self, caretaker_payload, api_client):
        response = api_client.post("/api/caretakers/", caretaker_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["full_name"] == caretaker_payload["full_name"]
        assert data["status"] == Caretaker.Status.ACTIVE
        assert "id" in data

    def test_create_caretaker_without_optional_fields(self, caretaker_optional_payload, api_client):
        response = api_client.post("/api/caretakers/", caretaker_optional_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["status"] == Caretaker.Status.ACTIVE
        assert data["full_name"] == caretaker_optional_payload["full_name"]

    def test_create_caretaker_missing_required_field(self, caretaker_payload, api_client):
        payload = caretaker_payload.copy()
        del payload["full_name"]
        response = api_client.post("/api/caretakers/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_caretaker_empty_required_field(self, caretaker_payload, api_client):
        payload = {**caretaker_payload, "full_name": ""}
        response = api_client.post("/api/caretakers/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_caretaker_returns_timestamps(self, caretaker_optional_payload, api_client):
        response = api_client.post("/api/caretakers/", caretaker_optional_payload, format="json")
        data = response.data
        assert "created_at" in data
        assert "updated_at" in data


class TestGetAllCaretakers:
    def test_get_all_returns_paginated_list(self, api_client):
        response = api_client.get("/api/caretakers/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_get_all_contains_created_caretaker(self, created_caretaker, api_client):
        response = api_client.get("/api/caretakers/")
        results = response.data["results"]
        ids = [item["id"] for item in results]
        assert created_caretaker["id"] in ids

    def test_get_all_caretaker_fields(self, created_caretaker, api_client):
        response = api_client.get("/api/caretakers/")
        results = response.data["results"]
        item = next((p for p in results if p["id"] == created_caretaker["id"]), None)
        assert item is not None
        for field in ("full_name", "id", "email"):
            assert field in item

    def test_get_all_filtering_by_status(self, created_caretaker, api_client):
        params = {"status": Caretaker.Status.ACTIVE}
        response = api_client.get("/api/caretakers/", params)
        results = response.data["results"]
        assert len(results) > 0
        for item in results:
            assert item["status"] == Caretaker.Status.ACTIVE


class TestGetCaretakerById:
    def test_get_caretaker_by_id_success(self, created_caretaker, api_client):
        caretaker_id = created_caretaker["id"]
        response = api_client.get(f"/api/caretakers/{caretaker_id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == caretaker_id

    def test_get_caretaker_by_id_not_found(self, api_client):
        response = api_client.get("/api/caretakers/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_caretaker_by_id_returns_correct_data(self, created_caretaker, api_client):
        response = api_client.get(f"/api/caretakers/{created_caretaker['id']}/")
        data = response.data
        assert data["full_name"] == created_caretaker["full_name"]


class TestUpdateCaretaker:
    def test_update_caretaker_by_id_success(self, created_caretaker, api_client):
        caretaker_id = created_caretaker["id"]
        update_payload = {"status": Caretaker.Status.BLOCKED}
        response = api_client.patch(f"/api/caretakers/{caretaker_id}/", update_payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data["status"] == Caretaker.Status.BLOCKED

    def test_update_caretaker_by_id_not_found(self, api_client):
        response = api_client.patch(
            "/api/caretakers/01ARZ3NDEKTSV4RRFFQ69G5FAV/",
            {"status": Caretaker.Status.BLOCKED},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_caretaker_updates_updated_at(self, created_caretaker, api_client):
        caretaker_id = created_caretaker["id"]
        original_updated_at = created_caretaker["updated_at"]
        time.sleep(2)
        api_client.patch(f"/api/caretakers/{caretaker_id}/", {"full_name": "nuevo nombre"}, format="json")
        response = api_client.get(f"/api/caretakers/{caretaker_id}/")
        new_updated_at = response.data["updated_at"]
        assert new_updated_at > original_updated_at

    def test_update_caretaker_invalid_status(self, created_caretaker, api_client):
        response = api_client.patch(
            f"/api/caretakers/{created_caretaker['id']}/", {"status": "INVALID"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestDeleteCaretaker:
    def test_delete_caretaker_by_id_success(self, caretaker_payload, api_client):
        create_resp = api_client.post("/api/caretakers/", caretaker_payload, format="json")
        caretaker_id = create_resp.data["id"]

        delete_resp = api_client.delete(f"/api/caretakers/{caretaker_id}/")
        assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

        get_resp = api_client.get(f"/api/caretakers/{caretaker_id}/")
        assert get_resp.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_caretaker_by_id_not_found(self, api_client):
        response = api_client.delete("/api/caretakers/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_caretaker_by_id_idempotent(self, caretaker_payload, api_client):
        create_resp = api_client.post("/api/caretakers/", caretaker_payload, format="json")
        caretaker_id = create_resp.data["id"]
        api_client.delete(f"/api/caretakers/{caretaker_id}/")
        second_delete = api_client.delete(f"/api/caretakers/{caretaker_id}/")
        assert second_delete.status_code == status.HTTP_404_NOT_FOUND
