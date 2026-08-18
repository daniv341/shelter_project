
from __future__ import annotations
import time
import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from vaccination_records.models import VaccinationRecord
from animals.models import Animal
from species.models import Species

pytestmark = pytest.mark.django_db


@pytest.fixture
def species(db):
    return Species.objects.create(name="gato", status="active")

@pytest.fixture
def animal(db, species):
        return Animal.objects.create(name="orion", sex="male", species=species, adoption_status="available", medical_status="healthy")

@pytest.fixture
def api_client() -> APIClient:
    return APIClient()

@pytest.fixture
def make_payload(animal):
    def _make_payload(**overrides) -> dict:
        """Payload minimo valido para crear un vaccination_record (todos los campos requeridos)."""
        payload = {
            "name": "Texto de prueba",
            "animal": animal.id,
            "status": "pending",
            "applied_at": "2026-08-17T19:16:27.889625"
        }
        payload.update(overrides)
        return payload

    return _make_payload

@pytest.fixture
def make_optional_only_payload(animal):
    def _make_optional_only_payload(**overrides) -> dict:
        """Payload solo con los campos requeridos, sin los opcionales."""
        payload = {
            "name": "Texto de prueba",
            "animal": animal.id,
            "status": "pending",
            "applied_at": "2026-08-17T19:16:27.889625"
        }
        payload.update(overrides)
        return payload

    return _make_optional_only_payload


@pytest.fixture
def vaccination_record_payload(make_payload) -> dict:
    return make_payload()

@pytest.fixture
def vaccination_record_optional_payload(make_optional_only_payload) -> dict:
    return make_optional_only_payload()


@pytest.fixture
def created_vaccination_record(vaccination_record_payload, api_client) -> dict:
    response = api_client.post("/api/vaccination_records/", vaccination_record_payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED, f"Setup fallo: {response.data}"
    return response.data


class TestCreateVaccinationRecord:
    def test_create_vaccination_record_success(self, vaccination_record_payload, api_client):
        response = api_client.post("/api/vaccination_records/", vaccination_record_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["name"] == vaccination_record_payload["name"]
        assert data["status"] == VaccinationRecord.Status.PENDING
        assert "id" in data

    def test_create_vaccination_record_without_optional_fields(self, vaccination_record_optional_payload, api_client):
        response = api_client.post("/api/vaccination_records/", vaccination_record_optional_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["status"] == VaccinationRecord.Status.PENDING
        assert data["name"] == vaccination_record_optional_payload["name"]

    def test_create_vaccination_record_missing_required_field(self, vaccination_record_payload, api_client):
        payload = vaccination_record_payload.copy()
        del payload["name"]
        response = api_client.post("/api/vaccination_records/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_vaccination_record_empty_required_field(self, vaccination_record_payload, api_client):
        payload = {**vaccination_record_payload, "name": ""}
        response = api_client.post("/api/vaccination_records/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_vaccination_record_with_invalid_date(
        self, make_payload, api_client) -> None:
        payload = make_payload(applied_at="17-08-2026 19:16:27")
        response = api_client.post("/api/vaccination_records/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_vaccination_record_returns_timestamps(self, vaccination_record_optional_payload, api_client):
        response = api_client.post("/api/vaccination_records/", vaccination_record_optional_payload, format="json")
        data = response.data
        assert "created_at" in data
        assert "updated_at" in data


class TestGetAllVaccinationRecords:
    def test_get_all_returns_paginated_list(self, api_client):
        response = api_client.get("/api/vaccination_records/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_get_all_contains_created_vaccination_record(self, created_vaccination_record, api_client):
        response = api_client.get("/api/vaccination_records/")
        results = response.data["results"]
        ids = [item["id"] for item in results]
        assert created_vaccination_record["id"] in ids

    def test_get_all_vaccination_record_fields(self, created_vaccination_record, api_client):
        response = api_client.get("/api/vaccination_records/")
        results = response.data["results"]
        item = next((p for p in results if p["id"] == created_vaccination_record["id"]), None)
        assert item is not None
        for field in ("name", "status", "animal"):
            assert field in item

    def test_get_all_filtering_by_status(self, created_vaccination_record, api_client):
        params = {"status": VaccinationRecord.Status.PENDING}
        response = api_client.get("/api/vaccination_records/", params)
        results = response.data["results"]
        assert len(results) > 0
        for item in results:
            assert item["status"] == VaccinationRecord.Status.PENDING


class TestGetVaccinationRecordById:
    def test_get_vaccination_record_by_id_success(self, created_vaccination_record, api_client):
        vaccination_record_id = created_vaccination_record["id"]
        response = api_client.get(f"/api/vaccination_records/{vaccination_record_id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == vaccination_record_id

    def test_get_vaccination_record_by_id_not_found(self, api_client):
        response = api_client.get("/api/vaccination_records/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_vaccination_record_by_id_returns_correct_data(self, created_vaccination_record, api_client):
        response = api_client.get(f"/api/vaccination_records/{created_vaccination_record['id']}/")
        data = response.data
        assert data["name"] == created_vaccination_record["name"]


class TestUpdateVaccinationRecord:
    def test_update_vaccination_record_by_id_success(self, created_vaccination_record, api_client):
        vaccination_record_id = created_vaccination_record["id"]
        update_payload = {"status": VaccinationRecord.Status.APPLIED}
        response = api_client.patch(f"/api/vaccination_records/{vaccination_record_id}/", update_payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data["status"] == VaccinationRecord.Status.APPLIED

    def test_update_vaccination_record_by_id_not_found(self, api_client):
        response = api_client.patch(
            "/api/vaccination_records/01ARZ3NDEKTSV4RRFFQ69G5FAV/",
            {"status": VaccinationRecord.Status.APPLIED},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_vaccination_record_updates_updated_at(self, created_vaccination_record, api_client):
        vaccination_record_id = created_vaccination_record["id"]
        original_updated_at = created_vaccination_record["updated_at"]
        time.sleep(2)
        api_client.patch(f"/api/vaccination_records/{vaccination_record_id}/", {"name": "Valor actualizado"}, format="json")
        response = api_client.get(f"/api/vaccination_records/{vaccination_record_id}/")
        new_updated_at = response.data["updated_at"]
        assert new_updated_at > original_updated_at

    def test_update_vaccination_record_invalid_status(self, created_vaccination_record, api_client):
        response = api_client.patch(
            f"/api/vaccination_records/{created_vaccination_record['id']}/", {"status": "INVALID"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestDeleteVaccinationRecord:
    def test_delete_vaccination_record_by_id_success(self, vaccination_record_payload, api_client):
        create_resp = api_client.post("/api/vaccination_records/", vaccination_record_payload, format="json")
        vaccination_record_id = create_resp.data["id"]

        delete_resp = api_client.delete(f"/api/vaccination_records/{vaccination_record_id}/")
        assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

        get_resp = api_client.get(f"/api/vaccination_records/{vaccination_record_id}/")
        assert get_resp.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_vaccination_record_by_id_not_found(self, api_client):
        response = api_client.delete("/api/vaccination_records/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_vaccination_record_by_id_idempotent(self, vaccination_record_payload, api_client):
        create_resp = api_client.post("/api/vaccination_records/", vaccination_record_payload, format="json")
        vaccination_record_id = create_resp.data["id"]
        api_client.delete(f"/api/vaccination_records/{vaccination_record_id}/")
        second_delete = api_client.delete(f"/api/vaccination_records/{vaccination_record_id}/")
        assert second_delete.status_code == status.HTTP_404_NOT_FOUND
