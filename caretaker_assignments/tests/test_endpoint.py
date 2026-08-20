
from __future__ import annotations
import time
import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from caretaker_assignments.models import CaretakerAssignment
from animals.models import Animal
from species.models import Species
from caretakers.models import Caretaker
from caretakers.models import Caretaker

pytestmark = pytest.mark.django_db

@pytest.fixture
def species(db):
    return Species.objects.create(name="gato", status="active")

@pytest.fixture
def animal(db, species):
        return Animal.objects.create(name="orion", sex="male", species=species, adoption_status="reserved", medical_status="healthy")

@pytest.fixture
def caretaker(db):
    return Caretaker.objects.create(full_name="rodrigo zurita", dni="12345678", status="active")

@pytest.fixture
def api_client() -> APIClient:
    return APIClient()

@pytest.fixture
def make_payload(animal, caretaker):
    def _make_payload(**overrides) -> dict:
        """Payload minimo valido para crear un caretaker_assignment (todos los campos requeridos)."""
        payload = {
            "animal": animal.id,
            "caretaker": caretaker.id,
            "status": CaretakerAssignment.Status.ACTIVE,
            "assingment_at": "2026-08-17T19:16:27.889625",
            "notes": "nota de prueba",
        }
        payload.update(overrides)
        return payload

    return _make_payload

@pytest.fixture
def make_optional_only_payload(animal, caretaker):
    def _make_optional_only_payload(**overrides) -> dict:
        """Payload solo con los campos requeridos, sin los opcionales."""
        payload = {
            "animal": animal.id,
            "caretaker": caretaker.id,
            "status": CaretakerAssignment.Status.ACTIVE,
        }
        payload.update(overrides)
        return payload

    return _make_optional_only_payload


@pytest.fixture
def caretaker_assignment_payload(make_payload) -> dict:
    return make_payload()

@pytest.fixture
def caretaker_assignment_optional_payload(make_optional_only_payload) -> dict:
    return make_optional_only_payload()
    
@pytest.fixture
def created_caretaker_assignment(caretaker_assignment_payload, api_client) -> dict:
    response = api_client.post("/api/caretaker_assignments/", caretaker_assignment_payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED, f"Setup fallo: {response.data}"
    return response.data


class TestCreateCaretakerAssignment:
    def test_create_caretaker_assignment_success(self, caretaker_assignment_payload, api_client):
        response = api_client.post("/api/caretaker_assignments/", caretaker_assignment_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["caretaker"]["id"] == caretaker_assignment_payload["caretaker"]
        assert data["status"] == CaretakerAssignment.Status.ACTIVE
        assert "id" in data

    def test_create_caretaker_assignment_without_optional_fields(self, caretaker_assignment_optional_payload, api_client):
        response = api_client.post("/api/caretaker_assignments/", caretaker_assignment_optional_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["status"] == CaretakerAssignment.Status.ACTIVE
        assert data["caretaker"]["id"] == caretaker_assignment_optional_payload["caretaker"]

    def test_create_caretaker_assignment_missing_required_field(self, caretaker_assignment_payload, api_client):
        payload = caretaker_assignment_payload.copy()
        del payload["caretaker"]
        response = api_client.post("/api/caretaker_assignments/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_caretaker_assignment_empty_required_field(self, caretaker_assignment_payload, api_client):
        payload = {**caretaker_assignment_payload, "caretaker": ""}
        response = api_client.post("/api/caretaker_assignments/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_caretaker_assignment_returns_timestamps(self, caretaker_assignment_optional_payload, api_client):
        response = api_client.post("/api/caretaker_assignments/", caretaker_assignment_optional_payload, format="json")
        data = response.data
        assert "created_at" in data
        assert "updated_at" in data


class TestGetAllCaretakerAssignments:
    def test_get_all_returns_paginated_list(self, api_client):
        response = api_client.get("/api/caretaker_assignments/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_get_all_contains_created_caretaker_assignment(self, created_caretaker_assignment, api_client):
        response = api_client.get("/api/caretaker_assignments/")
        results = response.data["results"]
        ids = [item["id"] for item in results]
        assert created_caretaker_assignment["id"] in ids

    def test_get_all_caretaker_assignment_fields(self, created_caretaker_assignment, api_client):
        response = api_client.get("/api/caretaker_assignments/")
        results = response.data["results"]
        item = next((p for p in results if p["id"] == created_caretaker_assignment["id"]), None)
        assert item is not None
        for field in ("animal", "caretaker", "status"):
            assert field in item

    def test_get_all_filtering_by_status(self, created_caretaker_assignment, api_client):
        params = {"status": CaretakerAssignment.Status.ACTIVE}
        response = api_client.get("/api/caretaker_assignments/", params)
        results = response.data["results"]
        assert len(results) > 0
        for item in results:
            assert item["status"] == CaretakerAssignment.Status.ACTIVE


class TestGetCaretakerAssignmentById:
    def test_get_caretaker_assignment_by_id_success(self, created_caretaker_assignment, api_client):
        caretaker_assignment_id = created_caretaker_assignment["id"]
        response = api_client.get(f"/api/caretaker_assignments/{caretaker_assignment_id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == caretaker_assignment_id

    def test_get_caretaker_assignment_by_id_not_found(self, api_client):
        response = api_client.get("/api/caretaker_assignments/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_caretaker_assignment_by_id_returns_correct_data(self, created_caretaker_assignment, api_client):
        response = api_client.get(f"/api/caretaker_assignments/{created_caretaker_assignment['id']}/")
        data = response.data
        assert data["caretaker"]["id"] == created_caretaker_assignment["caretaker"]["id"]


class TestUpdateCaretakerAssignment:
    def test_update_caretaker_assignment_by_id_success(self, created_caretaker_assignment, api_client):
        caretaker_assignment_id = created_caretaker_assignment["id"]
        update_payload = {"status": CaretakerAssignment.Status.FINISHED}
        response = api_client.patch(f"/api/caretaker_assignments/{caretaker_assignment_id}/", update_payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data["status"] == CaretakerAssignment.Status.FINISHED

    def test_update_caretaker_assignment_by_id_not_found(self, api_client):
        response = api_client.patch(
            "/api/caretaker_assignments/01ARZ3NDEKTSV4RRFFQ69G5FAV/",
            {"status": CaretakerAssignment.Status.FINISHED},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_caretaker_assignment_updates_updated_at(self, created_caretaker_assignment, api_client):
        caretaker_assignment_id = created_caretaker_assignment["id"]
        original_updated_at = created_caretaker_assignment["updated_at"]
        time.sleep(2)
        api_client.patch(f"/api/caretaker_assignments/{caretaker_assignment_id}/", {"notes": "nota actualizado"}, format="json")
        response = api_client.get(f"/api/caretaker_assignments/{caretaker_assignment_id}/")
        new_updated_at = response.data["updated_at"]
        assert new_updated_at > original_updated_at

    def test_update_caretaker_assignment_invalid_status(self, created_caretaker_assignment, api_client):
        response = api_client.patch(
            f"/api/caretaker_assignments/{created_caretaker_assignment['id']}/", {"status": "INVALID"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestDeleteCaretakerAssignment:
    def test_delete_caretaker_assignment_by_id_success(self, caretaker_assignment_payload, api_client):
        response = api_client.post("/api/caretaker_assignments/", caretaker_assignment_payload, format="json")
        caretaker_assignment_id = response.data["id"]

        delete_resp = api_client.delete(f"/api/caretaker_assignments/{caretaker_assignment_id}/")
        assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

        get_resp = api_client.get(f"/api/caretaker_assignments/{caretaker_assignment_id}/")
        assert get_resp.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_caretaker_assignment_by_id_not_found(self, api_client):
        response = api_client.delete("/api/caretaker_assignments/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_caretaker_assignment_by_id_idempotent(self, caretaker_assignment_payload, api_client):
        response = api_client.post("/api/caretaker_assignments/", caretaker_assignment_payload, format="json")
        caretaker_assignment_id = response.data["id"]
        api_client.delete(f"/api/caretaker_assignments/{caretaker_assignment_id}/")
        second_delete = api_client.delete(f"/api/caretaker_assignments/{caretaker_assignment_id}/")
        assert second_delete.status_code == status.HTTP_404_NOT_FOUND


@pytest.fixture
def animal_1(db, species):
        return Animal.objects.create(name="kity", sex="female", species=species, adoption_status="available", medical_status="healthy")

@pytest.fixture
def caretaker_1(db):
    return Caretaker.objects.create(full_name="micael rodriguez", dni="87654321", status="blocked")

class TestBusinessRules:
    def test_create_caretaker_assignment_with_animal_no_reserved(self, caretaker_assignment_payload, animal_1, api_client):
        payload = {**caretaker_assignment_payload, "animal": animal_1.id}
        response = api_client.post("/api/caretaker_assignments/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_caretaker_assignment_with_caretaker_blocked(self, caretaker_assignment_payload, caretaker_1, api_client):
        payload = {**caretaker_assignment_payload, "caretaker": caretaker_1.id}
        response = api_client.post("/api/caretaker_assignments/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_verified_caretaker_assignment_animal(self, caretaker_assignment_payload, api_client):
        response = api_client.post("/api/caretaker_assignments/", caretaker_assignment_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        animal_id = response.data["animal"]["id"]
        response = api_client.get(f"/api/animals/{animal_id}/")
        data = response.data
        assert data["adoption_status"] == Animal.AdoptionStatus.NOT_AVAILABLE

    def test_verified_caretaker_assignment_after_finished(self, caretaker_assignment_payload, created_caretaker_assignment, api_client):
        caretaker_assignment_id = created_caretaker_assignment["id"]
        update_payload = {"status": CaretakerAssignment.Status.FINISHED}
        response = api_client.patch(f"/api/caretaker_assignments/{caretaker_assignment_id}/", update_payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        response = api_client.post("/api/caretaker_assignments/", caretaker_assignment_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED


