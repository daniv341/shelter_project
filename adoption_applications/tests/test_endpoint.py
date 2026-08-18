
from __future__ import annotations
import time
import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from adoption_applications.models import AdoptionApplication
from animals.models import Animal
from species.models import Species
from adopters.models import Adopter

pytestmark = pytest.mark.django_db


@pytest.fixture
def species(db):
    return Species.objects.create(name="gato", status="active")

@pytest.fixture
def animal(db, species):
        return Animal.objects.create(name="orion", sex="male", species=species, adoption_status="available", medical_status="healthy")

@pytest.fixture
def adopter(db):
    return Adopter.objects.create(full_name="rodrigo zurita", dni="12345678", status="active")

@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def make_payload(animal, adopter):
    def _make_payload(**overrides) -> dict:
        """Payload minimo valido para crear un adoption_application (todos los campos requeridos)."""
        payload = {
            "animal": animal.id,
            "adopter": adopter.id,
            "status": AdoptionApplication.Status.SUBMITTED,
            "submitted_at": "2026-08-17T19:16:27.889625",
            "reviewed_at": "2026-09-17T19:16:27.889625",
            "description": "nota de prueba",
        }
        payload.update(overrides)
        return payload

    return _make_payload


@pytest.fixture
def make_optional_only_payload(animal, adopter):
    def _make_optional_only_payload(**overrides) -> dict:
        """Payload solo con los campos requeridos, sin los opcionales."""
        payload = {
            "animal": animal.id,
            "adopter": adopter.id,
            "status": AdoptionApplication.Status.SUBMITTED
        }
        payload.update(overrides)
        return payload

    return _make_optional_only_payload


@pytest.fixture
def adoption_application_payload(make_payload) -> dict:
    return make_payload()

@pytest.fixture
def adoption_application_optional_payload(make_optional_only_payload) -> dict:
    return make_optional_only_payload()
    
@pytest.fixture
def created_adoption_application(adoption_application_payload, api_client) -> dict:
    response = api_client.post("/api/adoption_applications/", adoption_application_payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED, f"Setup fallo: {response.data}"
    return response.data


class TestCreateAdoptionApplication:
    def test_create_adoption_application_success(self, adoption_application_payload, api_client):
        response = api_client.post("/api/adoption_applications/", adoption_application_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["animal"]["id"] == adoption_application_payload["animal"]
        assert data["status"] == AdoptionApplication.Status.SUBMITTED
        assert "id" in data

    def test_create_adoption_application_without_optional_fields(self, adoption_application_optional_payload, api_client):
        response = api_client.post("/api/adoption_applications/", adoption_application_optional_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["status"] == AdoptionApplication.Status.SUBMITTED
        assert data["animal"]["id"] == adoption_application_optional_payload["animal"]

    def test_create_adoption_application_missing_required_field(self, adoption_application_payload, api_client):
        payload = adoption_application_payload.copy()
        del payload["animal"]
        response = api_client.post("/api/adoption_applications/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_adoption_application_empty_required_field(self, adoption_application_payload, api_client):
        payload = {**adoption_application_payload, "animal": ""}
        response = api_client.post("/api/adoption_applications/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_adoption_application_returns_timestamps(self, adoption_application_optional_payload, api_client):
        response = api_client.post("/api/adoption_applications/", adoption_application_optional_payload, format="json")
        data = response.data
        assert "created_at" in data
        assert "updated_at" in data


class TestGetAllAdoptionApplications:
    def test_get_all_returns_paginated_list(self, api_client):
        response = api_client.get("/api/adoption_applications/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_get_all_contains_created_adoption_application(self, created_adoption_application, api_client):
        response = api_client.get("/api/adoption_applications/")
        results = response.data["results"]
        ids = [item["id"] for item in results]
        assert created_adoption_application["id"] in ids

    def test_get_all_adoption_application_fields(self, created_adoption_application, api_client):
        response = api_client.get("/api/adoption_applications/")
        results = response.data["results"]
        item = next((p for p in results if p["id"] == created_adoption_application["id"]), None)
        assert item is not None
        for field in ("animal", "adopter", "status"):
            assert field in item

    def test_get_all_filtering_by_status(self, created_adoption_application, api_client):
        params = {"status": AdoptionApplication.Status.SUBMITTED}
        response = api_client.get("/api/adoption_applications/", params)
        results = response.data["results"]
        assert len(results) > 0
        for item in results:
            assert item["status"] == AdoptionApplication.Status.SUBMITTED


class TestGetAdoptionApplicationById:
    def test_get_adoption_application_by_id_success(self, created_adoption_application, api_client):
        adoption_application_id = created_adoption_application["id"]
        response = api_client.get(f"/api/adoption_applications/{adoption_application_id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == adoption_application_id

    def test_get_adoption_application_by_id_not_found(self, api_client):
        response = api_client.get("/api/adoption_applications/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_adoption_application_by_id_returns_correct_data(self, created_adoption_application, api_client):
        response = api_client.get(f"/api/adoption_applications/{created_adoption_application['id']}/")
        data = response.data
        assert data["animal"]["id"] == created_adoption_application["animal"]["id"]


class TestUpdateAdoptionApplication:
    def test_update_adoption_application_by_id_success(self, created_adoption_application, api_client):
        adoption_application_id = created_adoption_application["id"]
        update_payload = {"status": AdoptionApplication.Status.REVISION}
        response = api_client.patch(f"/api/adoption_applications/{adoption_application_id}/", update_payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data["status"] == AdoptionApplication.Status.REVISION

    def test_update_adoption_application_by_id_not_found(self, api_client):
        response = api_client.patch(
            "/api/adoption_applications/01ARZ3NDEKTSV4RRFFQ69G5FAV/",
            {"status": AdoptionApplication.Status.REVISION},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_adoption_application_updates_updated_at(self, created_adoption_application, api_client):
        adoption_application_id = created_adoption_application["id"]
        original_updated_at = created_adoption_application["updated_at"]
        time.sleep(2)
        api_client.patch(f"/api/adoption_applications/{adoption_application_id}/", {"notes": "nota actualizada"}, format="json")
        response = api_client.get(f"/api/adoption_applications/{adoption_application_id}/")
        new_updated_at = response.data["updated_at"]
        assert new_updated_at > original_updated_at

    def test_update_adoption_application_invalid_status(self, created_adoption_application, api_client):
        response = api_client.patch(
            f"/api/adoption_applications/{created_adoption_application['id']}/", {"status": "INVALID"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestDeleteAdoptionApplication:
    def test_delete_adoption_application_by_id_success(self, adoption_application_payload, api_client):
        create_resp = api_client.post("/api/adoption_applications/", adoption_application_payload, format="json")
        adoption_application_id = create_resp.data["id"]

        delete_resp = api_client.delete(f"/api/adoption_applications/{adoption_application_id}/")
        assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

        get_resp = api_client.get(f"/api/adoption_applications/{adoption_application_id}/")
        assert get_resp.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_adoption_application_by_id_not_found(self, api_client):
        response = api_client.delete("/api/adoption_applications/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_adoption_application_by_id_idempotent(self, adoption_application_payload, api_client):
        create_resp = api_client.post("/api/adoption_applications/", adoption_application_payload, format="json")
        adoption_application_id = create_resp.data["id"]
        api_client.delete(f"/api/adoption_applications/{adoption_application_id}/")
        second_delete = api_client.delete(f"/api/adoption_applications/{adoption_application_id}/")
        assert second_delete.status_code == status.HTTP_404_NOT_FOUND
