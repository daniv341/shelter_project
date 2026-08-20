
from __future__ import annotations
import time
import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from adoption_events.models import AdoptionEvent
from animals.models import Animal
from species.models import Species
from adopters.models import Adopter
from adoption_applications.models import AdoptionApplication

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
def adoption_application(db, animal, adopter):
    return AdoptionApplication.objects.create(animal=animal, adopter=adopter, status="revision")

@pytest.fixture
def api_client() -> APIClient:
    return APIClient()

@pytest.fixture
def make_payload(animal, adopter, adoption_application):
    def _make_payload(**overrides) -> dict:
        """Payload minimo valido para crear un adoption_event (todos los campos requeridos)."""
        payload = {
            "animal": animal.id,
            "adopter": adopter.id,
            "adoption_application": adoption_application.id,
            "status": AdoptionEvent.Status.ONGOING,
            "adoption_at": "2026-08-17T19:16:27.889625",
            "notes": "nota de prueba",
        }
        payload.update(overrides)
        return payload

    return _make_payload

@pytest.fixture
def make_optional_only_payload(animal, adopter, adoption_application):
    def _make_optional_only_payload(**overrides) -> dict:
        """Payload solo con los campos requeridos, sin los opcionales."""
        payload = {
            "animal": animal.id,
            "adopter": adopter.id,
            "adoption_application": adoption_application.id,
            "status": AdoptionEvent.Status.ONGOING,
        }
        payload.update(overrides)
        return payload

    return _make_optional_only_payload


@pytest.fixture
def adoption_event_payload(make_payload) -> dict:
    return make_payload()

@pytest.fixture
def adoption_event_optional_payload(make_optional_only_payload) -> dict:
    return make_optional_only_payload()
    
@pytest.fixture
def created_adoption_event(adoption_event_payload, api_client) -> dict:
    response = api_client.post("/api/adoption_events/", adoption_event_payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED, f"Setup fallo: {response.data}"
    return response.data


class TestCreateAdoptionEvent:
    def test_create_adoption_event_success(self, adoption_event_payload, api_client):
        response = api_client.post("/api/adoption_events/", adoption_event_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["animal"]["id"] == adoption_event_payload["animal"]
        assert data["status"] == AdoptionEvent.Status.ONGOING
        assert "id" in data

    def test_create_adoption_event_without_optional_fields(self, adoption_event_optional_payload, api_client):
        response = api_client.post("/api/adoption_events/", adoption_event_optional_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["status"] == AdoptionEvent.Status.ONGOING
        assert data["animal"]["id"] == adoption_event_optional_payload["animal"]

    def test_create_adoption_event_missing_required_field(self, adoption_event_payload, api_client):
        payload = adoption_event_payload.copy()
        del payload["animal"]
        response = api_client.post("/api/adoption_events/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_adoption_event_empty_required_field(self, adoption_event_payload, api_client):
        payload = {**adoption_event_payload, "animal": ""}
        response = api_client.post("/api/adoption_events/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_adoption_event_returns_timestamps(self, adoption_event_optional_payload, api_client):
        response = api_client.post("/api/adoption_events/", adoption_event_optional_payload, format="json")
        data = response.data
        assert "created_at" in data
        assert "updated_at" in data


class TestGetAllAdoptionEvents:
    def test_get_all_returns_paginated_list(self, api_client):
        response = api_client.get("/api/adoption_events/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_get_all_contains_created_adoption_event(self, created_adoption_event, api_client):
        response = api_client.get("/api/adoption_events/")
        results = response.data["results"]
        ids = [item["id"] for item in results]
        assert created_adoption_event["id"] in ids

    def test_get_all_adoption_event_fields(self, created_adoption_event, api_client):
        response = api_client.get("/api/adoption_events/")
        results = response.data["results"]
        item = next((p for p in results if p["id"] == created_adoption_event["id"]), None)
        assert item is not None
        for field in ("animal", "adopter", "status", "adoption_application"):
            assert field in item

    def test_get_all_filtering_by_status(self, created_adoption_event, api_client):
        params = {"status": AdoptionEvent.Status.ONGOING}
        response = api_client.get("/api/adoption_events/", params)
        results = response.data["results"]
        assert len(results) > 0
        for item in results:
            assert item["status"] == AdoptionEvent.Status.ONGOING


class TestGetAdoptionEventById:
    def test_get_adoption_event_by_id_success(self, created_adoption_event, api_client):
        adoption_event_id = created_adoption_event["id"]
        response = api_client.get(f"/api/adoption_events/{adoption_event_id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == adoption_event_id

    def test_get_adoption_event_by_id_not_found(self, api_client):
        response = api_client.get("/api/adoption_events/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_adoption_event_by_id_returns_correct_data(self, created_adoption_event, api_client):
        response = api_client.get(f"/api/adoption_events/{created_adoption_event['id']}/")
        data = response.data
        assert data["animal"]["id"] == created_adoption_event["animal"]["id"]


class TestUpdateAdoptionEvent:
    def test_update_adoption_event_by_id_success(self, created_adoption_event, api_client):
        adoption_event_id = created_adoption_event["id"]
        update_payload = {"status": AdoptionEvent.Status.CLOSED}
        response = api_client.patch(f"/api/adoption_events/{adoption_event_id}/", update_payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data["status"] == AdoptionEvent.Status.CLOSED

    def test_update_adoption_event_by_id_not_found(self, api_client):
        response = api_client.patch(
            "/api/adoption_events/01ARZ3NDEKTSV4RRFFQ69G5FAV/",
            {"status": AdoptionEvent.Status.CLOSED},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_adoption_event_updates_updated_at(self, created_adoption_event, api_client):
        adoption_event_id = created_adoption_event["id"]
        original_updated_at = created_adoption_event["updated_at"]
        time.sleep(2)
        api_client.patch(f"/api/adoption_events/{adoption_event_id}/", {"notes": "nota actualizado"}, format="json")
        response = api_client.get(f"/api/adoption_events/{adoption_event_id}/")
        new_updated_at = response.data["updated_at"]
        assert new_updated_at > original_updated_at

    def test_update_adoption_event_invalid_status(self, created_adoption_event, api_client):
        response = api_client.patch(
            f"/api/adoption_events/{created_adoption_event['id']}/", {"status": "INVALID"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestDeleteAdoptionEvent:
    def test_delete_adoption_event_by_id_success(self, adoption_event_payload, api_client):
        create_resp = api_client.post("/api/adoption_events/", adoption_event_payload, format="json")
        adoption_event_id = create_resp.data["id"]

        delete_resp = api_client.delete(f"/api/adoption_events/{adoption_event_id}/")
        assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

        get_resp = api_client.get(f"/api/adoption_events/{adoption_event_id}/")
        assert get_resp.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_adoption_event_by_id_not_found(self, api_client):
        response = api_client.delete("/api/adoption_events/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_adoption_event_by_id_idempotent(self, adoption_event_payload, api_client):
        create_resp = api_client.post("/api/adoption_events/", adoption_event_payload, format="json")
        adoption_event_id = create_resp.data["id"]
        api_client.delete(f"/api/adoption_events/{adoption_event_id}/")
        second_delete = api_client.delete(f"/api/adoption_events/{adoption_event_id}/")
        assert second_delete.status_code == status.HTTP_404_NOT_FOUND


@pytest.fixture
def animal_1(db, species):
        return Animal.objects.create(name="kity", sex="female", species=species, adoption_status="adopted", medical_status="healthy")

@pytest.fixture
def animal_2(db, species):
        return Animal.objects.create(name="timoteo", sex="male", species=species, adoption_status="available", medical_status="in_treatment")

@pytest.fixture
def adopter_1(db):
    return Adopter.objects.create(full_name="micael rodriguez", dni="87654321", status="blocked")

@pytest.fixture
def adoption_application_1(db, animal, adopter):
    return AdoptionApplication.objects.create(animal=animal, adopter=adopter, status="submitted")

class TestBusinessRules:
    def test_create_adoption_event_with_animal_adopted(self, adoption_event_payload, animal_1, api_client):
        payload = {**adoption_event_payload, "animal": animal_1.id}
        response = api_client.post("/api/adoption_events/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_adoption_event_with_animal_no_healthy(self, adoption_event_payload, animal_2, api_client):
        payload = {**adoption_event_payload, "animal": animal_2.id}
        response = api_client.post("/api/adoption_events/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_adoption_event_with_adopter_blocked(self, adoption_event_payload, adopter_1, api_client):
        payload = {**adoption_event_payload, "adopter": adopter_1.id}
        response = api_client.post("/api/adoption_events/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_adoption_event_with_adoption_application_no_revision(self, adoption_event_payload,adoption_application_1, api_client):
        payload = {**adoption_event_payload, "adoption_application": adoption_application_1.id}
        response = api_client.post("/api/adoption_events/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_adoption_event_closed(self, adoption_event_payload, api_client):
        payload = {**adoption_event_payload, "status": "closed"}
        response = api_client.post("/api/adoption_events/", payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        adoption_event_id = response.data["id"]
        update_payload = {"notes": "nota actualizada"}
        response = api_client.patch(f"/api/adoption_events/{adoption_event_id}/", update_payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_verified_adoption_event_animal(self, created_adoption_event, api_client):
        adoption_event_id = created_adoption_event["id"]
        payload = {"status": AdoptionEvent.Status.CLOSED}
        response_primary = api_client.patch(f"/api/adoption_events/{adoption_event_id}/", payload, format="json")
        assert response_primary.status_code == status.HTTP_200_OK
        animal_id = response_primary.data["animal"]["id"]
        response = api_client.get(f"/api/animals/{animal_id}/")
        data = response.data
        assert data["adoption_status"] == Animal.AdoptionStatus.ADOPTED
        adoption_application_id = response_primary.data["adoption_application"]["id"]
        response = api_client.get(f"/api/adoption_applications/{adoption_application_id}/")
        data = response.data
        assert data["status"] == AdoptionApplication.Status.CLOSED
