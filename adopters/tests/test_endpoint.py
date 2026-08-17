from __future__ import annotations
import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from adopters.models import Adopter

# esta linea lo que hace es crear una base de datos de prueba que hace rollback al final de todo, es decir no quedara nada despues, solo hace los test y se muere
pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


def make_payload(**overrides) -> dict:
    """Payload minimo valido para crear un adopter (todos los campos requeridos)."""
    payload = {
        "full_name": "nombre de prueba",
        "dni": f"{uuid.uuid4().int % 10000000}",
        "email": f"test_{uuid.uuid4().hex[:5]}@gmail.com",
        "phone": "381123456",
        "status": Adopter.Status.ACTIVE,
    }
    payload.update(overrides)
    return payload


def make_optional_only_payload(**overrides) -> dict:
    """Payload solo con los campos requeridos, sin los opcionales."""
    payload = {
        "full_name": "nombre de prueba",
        "dni": f"{uuid.uuid4().int % 10000000}",
        "email": f"test_{uuid.uuid4().hex[:5]}@gmail.com",
        "status": Adopter.Status.ACTIVE,
    }
    payload.update(overrides)
    return payload


@pytest.fixture
def adopter_payload() -> dict:
    return make_payload()


@pytest.fixture
def created_adopter(adopter_payload, api_client) -> dict:
    response = api_client.post("/api/adopters/", adopter_payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED, f"Setup fallo: {response.data}"
    return response.data


class TestCreateAdopter:
    def test_create_adopter_success(self, adopter_payload, api_client):
        response = api_client.post("/api/adopters/", adopter_payload, format="json")
        print("STATUS:", response.status_code)
        print("COUNT:", Adopter.objects.count())
        print("ADOPTERS:", list(Adopter.objects.values()))
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["full_name"] == adopter_payload["full_name"]
        assert data["status"] == Adopter.Status.ACTIVE
        assert "id" in data

    def test_create_adopter_without_optional_fields(self, api_client):
        payload = make_optional_only_payload()
        response = api_client.post("/api/adopters/", payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["status"] == Adopter.Status.ACTIVE
        assert data["full_name"] == payload["full_name"]

    def test_create_adopter_missing_required_field(self, adopter_payload, api_client):
        payload = adopter_payload.copy()
        del payload["full_name"]
        response = api_client.post("/api/adopters/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_adopter_empty_required_field(self, adopter_payload, api_client):
        payload = {**adopter_payload, "full_name": ""}
        response = api_client.post("/api/adopters/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_adopter_returns_timestamps(self, api_client):
        payload = make_optional_only_payload()
        response = api_client.post("/api/adopters/", payload, format="json")
        data = response.data
        assert "created_at" in data
        assert "updated_at" in data


class TestGetAllAdopters:
    def test_get_all_returns_paginated_list(self, api_client):
        response = api_client.get("/api/adopters/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_get_all_contains_created_adopter(self, created_adopter, api_client):
        response = api_client.get("/api/adopters/")
        results = response.data["results"]
        ids = [item["id"] for item in results]
        assert created_adopter["id"] in ids

    def test_get_all_adopter_fields(self, created_adopter, api_client):
        response = api_client.get("/api/adopters/")
        results = response.data["results"]
        item = next((p for p in results if p["id"] == created_adopter["id"]), None)
        assert item is not None
        for field in ("full_name", "id", "email"):
            assert field in item

    def test_get_all_filtering_by_status(self, created_adopter, api_client):
        params = {"status": Adopter.Status.ACTIVE}
        response = api_client.get("/api/adopters/", params)
        results = response.data["results"]
        assert len(results) > 0
        for item in results:
            assert item["status"] == Adopter.Status.ACTIVE


class TestGetAdopterById:
    def test_get_adopter_by_id_success(self, created_adopter, api_client):
        adopter_id = created_adopter["id"]
        response = api_client.get(f"/api/adopters/{adopter_id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == adopter_id

    def test_get_adopter_by_id_not_found(self, api_client):
        response = api_client.get("/api/adopters/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_adopter_by_id_returns_correct_data(self, created_adopter, api_client):
        response = api_client.get(f"/api/adopters/{created_adopter['id']}/")
        data = response.data
        assert data["full_name"] == created_adopter["full_name"]


class TestUpdateAdopter:
    def test_update_adopter_by_id_success(self, created_adopter, api_client):
        adopter_id = created_adopter["id"]
        update_payload = {"status": Adopter.Status.BLOCKED}
        response = api_client.patch(f"/api/adopters/{adopter_id}/", update_payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data["status"] == Adopter.Status.BLOCKED

    def test_update_adopter_by_id_not_found(self, api_client):
        response = api_client.patch(
            "/api/adopters/01ARZ3NDEKTSV4RRFFQ69G5FAV/",
            {"status": Adopter.Status.BLOCKED},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_adopter_updates_updated_at(self, created_adopter, api_client):
        adopter_id = created_adopter["id"]
        original_updated_at = created_adopter["updated_at"]
        api_client.patch(f"/api/adopters/{adopter_id}/", {"full_name": "nuevo nombre"}, format="json")
        response = api_client.get(f"/api/adopters/{adopter_id}/")
        new_updated_at = response.data["updated_at"]
        assert new_updated_at >= original_updated_at

    def test_update_adopter_invalid_status(self, created_adopter, api_client):
        response = api_client.patch(
            f"/api/adopters/{created_adopter['id']}/", {"status": "INVALID"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestDeleteAdopter:
    def test_delete_adopter_by_id_success(self, adopter_payload, api_client):
        create_resp = api_client.post("/api/adopters/", adopter_payload, format="json")
        adopter_id = create_resp.data["id"]

        delete_resp = api_client.delete(f"/api/adopters/{adopter_id}/")
        assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

        get_resp = api_client.get(f"/api/adopters/{adopter_id}/")
        assert get_resp.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_adopter_by_id_not_found(self, api_client):
        response = api_client.delete("/api/adopters/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_adopter_by_id_idempotent(self, adopter_payload, api_client):
        create_resp = api_client.post("/api/adopters/", adopter_payload, format="json")
        adopter_id = create_resp.data["id"]
        api_client.delete(f"/api/adopters/{adopter_id}/")
        second_delete = api_client.delete(f"/api/adopters/{adopter_id}/")
        assert second_delete.status_code == status.HTTP_404_NOT_FOUND
