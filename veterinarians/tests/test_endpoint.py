
from __future__ import annotations
import time
import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from veterinarians.models import Veterinatian

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


def make_payload(**overrides) -> dict:
    """Payload minimo valido para crear un veterinatian (todos los campos requeridos)."""
    payload = {
        "full_name": "nombre de prueba",
        "dni": f"{uuid.uuid4().int % 10000000}",
        "email": f"test_{uuid.uuid4().hex[:5]}@gmail.com",
        "phone": "381123456",
        "status": Veterinatian.Status.ACTIVE,
    }
    payload.update(overrides)
    return payload


def make_optional_only_payload(**overrides) -> dict:
    """Payload solo con los campos requeridos, sin los opcionales."""
    payload = {
        "full_name": "nombre de prueba",
        "dni": f"{uuid.uuid4().int % 10000000}",
        "status": Veterinatian.Status.ACTIVE,
    }
    payload.update(overrides)
    return payload


@pytest.fixture
def veterinatian_payload() -> dict:
    return make_payload()


@pytest.fixture
def created_veterinatian(veterinatian_payload, api_client) -> dict:
    response = api_client.post("/api/veterinarians/", veterinatian_payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED, f"Setup fallo: {response.data}"
    return response.data


class TestCreateVeterinatian:
    def test_create_veterinatian_success(self, veterinatian_payload, api_client):
        response = api_client.post("/api/veterinarians/", veterinatian_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["full_name"] == veterinatian_payload["full_name"]
        assert data["status"] == Veterinatian.Status.ACTIVE
        assert "id" in data

    def test_create_veterinatian_without_optional_fields(self, api_client):
        payload = make_optional_only_payload()
        response = api_client.post("/api/veterinarians/", payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["status"] == Veterinatian.Status.ACTIVE
        assert data["full_name"] == payload["full_name"]

    def test_create_veterinatian_missing_required_field(self, veterinatian_payload, api_client):
        payload = veterinatian_payload.copy()
        del payload["full_name"]
        response = api_client.post("/api/veterinarians/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_veterinatian_empty_required_field(self, veterinatian_payload, api_client):
        payload = {**veterinatian_payload, "full_name": ""}
        response = api_client.post("/api/veterinarians/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_veterinatian_returns_timestamps(self, api_client):
        payload = make_optional_only_payload()
        response = api_client.post("/api/veterinarians/", payload, format="json")
        data = response.data
        assert "created_at" in data
        assert "updated_at" in data


class TestGetAllVeterinarians:
    def test_get_all_returns_paginated_list(self, api_client):
        response = api_client.get("/api/veterinarians/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_get_all_contains_created_veterinatian(self, created_veterinatian, api_client):
        response = api_client.get("/api/veterinarians/")
        results = response.data["results"]
        ids = [item["id"] for item in results]
        assert created_veterinatian["id"] in ids

    def test_get_all_veterinatian_fields(self, created_veterinatian, api_client):
        response = api_client.get("/api/veterinarians/")
        results = response.data["results"]
        item = next((p for p in results if p["id"] == created_veterinatian["id"]), None)
        assert item is not None
        for field in ("full_name",):
            assert field in item

    def test_get_all_filtering_by_status(self, created_veterinatian, api_client):
        params = {"status": Veterinatian.Status.ACTIVE}
        response = api_client.get("/api/veterinarians/", params)
        results = response.data["results"]
        assert len(results) > 0
        for item in results:
            assert item["status"] == Veterinatian.Status.ACTIVE


class TestGetVeterinatianById:
    def test_get_veterinatian_by_id_success(self, created_veterinatian, api_client):
        veterinatian_id = created_veterinatian["id"]
        response = api_client.get(f"/api/veterinarians/{veterinatian_id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == veterinatian_id

    def test_get_veterinatian_by_id_not_found(self, api_client):
        response = api_client.get("/api/veterinarians/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_veterinatian_by_id_returns_correct_data(self, created_veterinatian, api_client):
        response = api_client.get(f"/api/veterinarians/{created_veterinatian['id']}/")
        data = response.data
        assert data["full_name"] == created_veterinatian["full_name"]


class TestUpdateVeterinatian:
    def test_update_veterinatian_by_id_success(self, created_veterinatian, api_client):
        veterinatian_id = created_veterinatian["id"]
        update_payload = {"status": Veterinatian.Status.BLOCKED}
        response = api_client.patch(f"/api/veterinarians/{veterinatian_id}/", update_payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data["status"] == Veterinatian.Status.BLOCKED

    def test_update_veterinatian_by_id_not_found(self, api_client):
        response = api_client.patch(
            "/api/veterinarians/01ARZ3NDEKTSV4RRFFQ69G5FAV/",
            {"status": Veterinatian.Status.BLOCKED},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_veterinatian_updates_updated_at(self, created_veterinatian, api_client):
        veterinatian_id = created_veterinatian["id"]
        original_updated_at = created_veterinatian["updated_at"]
        time.sleep(2)
        api_client.patch(f"/api/veterinarians/{veterinatian_id}/", {"full_name": "nombre actualizado"}, format="json")
        response = api_client.get(f"/api/veterinarians/{veterinatian_id}/")
        new_updated_at = response.data["updated_at"]
        assert new_updated_at > original_updated_at

    def test_update_veterinatian_invalid_status(self, created_veterinatian, api_client):
        response = api_client.patch(
            f"/api/veterinarians/{created_veterinatian['id']}/", {"status": "INVALID"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestDeleteVeterinatian:
    def test_delete_veterinatian_by_id_success(self, veterinatian_payload, api_client):
        create_resp = api_client.post("/api/veterinarians/", veterinatian_payload, format="json")
        veterinatian_id = create_resp.data["id"]

        delete_resp = api_client.delete(f"/api/veterinarians/{veterinatian_id}/")
        assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

        get_resp = api_client.get(f"/api/veterinarians/{veterinatian_id}/")
        assert get_resp.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_veterinatian_by_id_not_found(self, api_client):
        response = api_client.delete("/api/veterinarians/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_veterinatian_by_id_idempotent(self, veterinatian_payload, api_client):
        create_resp = api_client.post("/api/veterinarians/", veterinatian_payload, format="json")
        veterinatian_id = create_resp.data["id"]
        api_client.delete(f"/api/veterinarians/{veterinatian_id}/")
        second_delete = api_client.delete(f"/api/veterinarians/{veterinatian_id}/")
        assert second_delete.status_code == status.HTTP_404_NOT_FOUND
