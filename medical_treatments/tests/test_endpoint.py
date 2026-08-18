
from __future__ import annotations
import time
import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from medical_treatments.models import MedicalTreatment
from animals.models import Animal
from species.models import Species
from veterinarians.models import Veterinarian

pytestmark = pytest.mark.django_db


@pytest.fixture
def species(db):
    return Species.objects.create(name="gato", status="active")

@pytest.fixture
def animal(db, species):
        return Animal.objects.create(name="orion", sex="male", species=species, adoption_status="available", medical_status="healthy")

@pytest.fixture
def veterinarian(db):
    return Veterinarian.objects.create(full_name="rodrigo zurita", dni="12345678", status="active")

@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def make_payload(animal, veterinarian):
    def _make_payload(**overrides) -> dict:
        """Payload minimo valido para crear un medical_treatment (todos los campos requeridos)."""
        payload = {
            "diagnostic": "Texto de prueba",
            "animal": animal.id,
            "veterinarian": veterinarian.id,
            "status": MedicalTreatment.Status.PENDING,
            "description": "descripcion de prueba",
            "started_at": "2026-08-17T19:16:27.889625",
            "ended_at": "2026-09-17T19:16:27.889625",
        }
        payload.update(overrides)
        return payload

    return _make_payload

@pytest.fixture
def make_optional_only_payload(animal, veterinarian):
    def _make_optional_only_payload(**overrides) -> dict:
        """Payload solo con los campos requeridos, sin los opcionales."""
        payload = {
            "diagnostic": "Texto de prueba",
            "animal": animal.id,
            "veterinarian": veterinarian.id,
            "status": MedicalTreatment.Status.PENDING,
        }
        payload.update(overrides)
        return payload

    return _make_optional_only_payload


@pytest.fixture
def medical_treatment_payload(make_payload) -> dict:
    return make_payload()

@pytest.fixture
def medical_treatment_optional_payload(make_optional_only_payload) -> dict:
    return make_optional_only_payload()
    
@pytest.fixture
def created_medical_treatment(medical_treatment_payload, api_client) -> dict:
    response = api_client.post("/api/medical_treatments/", medical_treatment_payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED, f"Setup fallo: {response.data}"
    return response.data


class TestCreateMedicalTreatment:
    def test_create_medical_treatment_success(self, medical_treatment_payload, api_client):
        response = api_client.post("/api/medical_treatments/", medical_treatment_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["diagnostic"] == medical_treatment_payload["diagnostic"]
        assert data["status"] == MedicalTreatment.Status.PENDING
        assert "id" in data

    def test_create_medical_treatment_without_optional_fields(self, medical_treatment_optional_payload, api_client):
        response = api_client.post("/api/medical_treatments/", medical_treatment_optional_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["status"] == MedicalTreatment.Status.PENDING
        assert data["diagnostic"] == medical_treatment_optional_payload["diagnostic"]

    def test_create_medical_treatment_missing_required_field(self, medical_treatment_payload, api_client):
        payload = medical_treatment_payload.copy()
        del payload["diagnostic"]
        response = api_client.post("/api/medical_treatments/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_medical_treatment_empty_required_field(self, medical_treatment_payload, api_client):
        payload = {**medical_treatment_payload, "diagnostic": ""}
        response = api_client.post("/api/medical_treatments/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_medical_treatment_returns_timestamps(self, medical_treatment_optional_payload, api_client):
        response = api_client.post("/api/medical_treatments/", medical_treatment_optional_payload, format="json")
        data = response.data
        assert "created_at" in data
        assert "updated_at" in data


class TestGetAllMedicalTreatments:
    def test_get_all_returns_paginated_list(self, api_client):
        response = api_client.get("/api/medical_treatments/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_get_all_contains_created_medical_treatment(self, created_medical_treatment, api_client):
        response = api_client.get("/api/medical_treatments/")
        results = response.data["results"]
        ids = [item["id"] for item in results]
        assert created_medical_treatment["id"] in ids

    def test_get_all_medical_treatment_fields(self, created_medical_treatment, api_client):
        response = api_client.get("/api/medical_treatments/")
        results = response.data["results"]
        item = next((p for p in results if p["id"] == created_medical_treatment["id"]), None)
        assert item is not None
        for field in ("diagnostic", "animal", "veterinarian"):
            assert field in item

    def test_get_all_filtering_by_status(self, created_medical_treatment, api_client):
        params = {"status": MedicalTreatment.Status.PENDING}
        response = api_client.get("/api/medical_treatments/", params)
        results = response.data["results"]
        assert len(results) > 0
        for item in results:
            assert item["status"] == MedicalTreatment.Status.PENDING


class TestGetMedicalTreatmentById:
    def test_get_medical_treatment_by_id_success(self, created_medical_treatment, api_client):
        medical_treatment_id = created_medical_treatment["id"]
        response = api_client.get(f"/api/medical_treatments/{medical_treatment_id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == medical_treatment_id

    def test_get_medical_treatment_by_id_not_found(self, api_client):
        response = api_client.get("/api/medical_treatments/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_medical_treatment_by_id_returns_correct_data(self, created_medical_treatment, api_client):
        response = api_client.get(f"/api/medical_treatments/{created_medical_treatment['id']}/")
        data = response.data
        assert data["diagnostic"] == created_medical_treatment["diagnostic"]


class TestUpdateMedicalTreatment:
    def test_update_medical_treatment_by_id_success(self, created_medical_treatment, api_client):
        medical_treatment_id = created_medical_treatment["id"]
        update_payload = {"status": MedicalTreatment.Status.STARTED}
        response = api_client.patch(f"/api/medical_treatments/{medical_treatment_id}/", update_payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data["status"] == MedicalTreatment.Status.STARTED

    def test_update_medical_treatment_by_id_not_found(self, api_client):
        response = api_client.patch(
            "/api/medical_treatments/01ARZ3NDEKTSV4RRFFQ69G5FAV/",
            {"status": MedicalTreatment.Status.STARTED},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_medical_treatment_updates_updated_at(self, created_medical_treatment, api_client):
        medical_treatment_id = created_medical_treatment["id"]
        original_updated_at = created_medical_treatment["updated_at"]
        time.sleep(2)
        api_client.patch(f"/api/medical_treatments/{medical_treatment_id}/", {"diagnostic": "Valor actualizado"}, format="json")
        response = api_client.get(f"/api/medical_treatments/{medical_treatment_id}/")
        new_updated_at = response.data["updated_at"]
        assert new_updated_at > original_updated_at

    def test_update_medical_treatment_invalid_status(self, created_medical_treatment, api_client):
        response = api_client.patch(
            f"/api/medical_treatments/{created_medical_treatment['id']}/", {"status": "INVALID"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestDeleteMedicalTreatment:
    def test_delete_medical_treatment_by_id_success(self, medical_treatment_payload, api_client):
        create_resp = api_client.post("/api/medical_treatments/", medical_treatment_payload, format="json")
        medical_treatment_id = create_resp.data["id"]

        delete_resp = api_client.delete(f"/api/medical_treatments/{medical_treatment_id}/")
        assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

        get_resp = api_client.get(f"/api/medical_treatments/{medical_treatment_id}/")
        assert get_resp.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_medical_treatment_by_id_not_found(self, api_client):
        response = api_client.delete("/api/medical_treatments/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_medical_treatment_by_id_idempotent(self, medical_treatment_payload, api_client):
        create_resp = api_client.post("/api/medical_treatments/", medical_treatment_payload, format="json")
        medical_treatment_id = create_resp.data["id"]
        api_client.delete(f"/api/medical_treatments/{medical_treatment_id}/")
        second_delete = api_client.delete(f"/api/medical_treatments/{medical_treatment_id}/")
        assert second_delete.status_code == status.HTTP_404_NOT_FOUND
