from __future__ import annotations
import time
import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from species.models import Species
from animals.models import Animal

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


def make_payload(**overrides) -> dict:
    """Payload minimo valido para crear un species (todos los campos requeridos)."""
    payload = {
        "name": "especie de prueba",
        "status": Species.Status.ACTIVE,
    }
    payload.update(overrides)
    return payload


@pytest.fixture
def species_payload() -> dict:
    return make_payload()


@pytest.fixture
def created_species(species_payload, api_client) -> dict:
    response = api_client.post("/api/species/", species_payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED, f"Setup fallo: {response.data}"
    return response.data


class TestCreateSpecies:
    def test_create_species_success(self, species_payload, api_client):
        response = api_client.post("/api/species/", species_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["name"] == species_payload["name"]
        assert data["status"] == Species.Status.ACTIVE
        assert "id" in data

    def test_create_species_missing_required_field(self, species_payload, api_client):
        payload = species_payload.copy()
        del payload["name"]
        response = api_client.post("/api/species/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_species_empty_required_field(self, species_payload, api_client):
        payload = {**species_payload, "name": ""}
        response = api_client.post("/api/species/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_species_returns_timestamps(self, api_client):
        payload = make_payload()
        response = api_client.post("/api/species/", payload, format="json")
        data = response.data
        assert "created_at" in data
        assert "updated_at" in data


class TestGetAllSpecies:
    def test_get_all_returns_paginated_list(self, api_client):
        response = api_client.get("/api/species/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_get_all_contains_created_species(self, created_species, api_client):
        response = api_client.get("/api/species/")
        results = response.data["results"]
        ids = [item["id"] for item in results]
        assert created_species["id"] in ids

    def test_get_all_species_fields(self, created_species, api_client):
        response = api_client.get("/api/species/")
        results = response.data["results"]
        item = next((p for p in results if p["id"] == created_species["id"]), None)
        assert item is not None
        for field in ("name", "status", "id"):
            assert field in item

    def test_get_all_filtering_by_status(self, created_species, api_client):
        params = {"status": Species.Status.ACTIVE}
        response = api_client.get("/api/species/", params)
        results = response.data["results"]
        assert len(results) > 0
        for item in results:
            assert item["status"] == Species.Status.ACTIVE


class TestGetSpeciesById:
    def test_get_species_by_id_success(self, created_species, api_client):
        species_id = created_species["id"]
        response = api_client.get(f"/api/species/{species_id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == species_id

    def test_get_species_by_id_not_found(self, api_client):
        response = api_client.get("/api/species/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_species_by_id_returns_correct_data(self, created_species, api_client):
        response = api_client.get(f"/api/species/{created_species['id']}/")
        data = response.data
        assert data["name"] == created_species["name"]


class TestUpdateSpecies:
    def test_update_species_by_id_success(self, created_species, api_client):
        species_id = created_species["id"]
        update_payload = {"status": Species.Status.BLOCKED}
        response = api_client.patch(f"/api/species/{species_id}/", update_payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data["status"] == Species.Status.BLOCKED

    def test_update_species_by_id_not_found(self, api_client):
        response = api_client.patch(
            "/api/species/01ARZ3NDEKTSV4RRFFQ69G5FAV/",
            {"status": Species.Status.BLOCKED},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_species_updates_updated_at(self, created_species, api_client):
        species_id = created_species["id"]
        original_updated_at = created_species["updated_at"]
        time.sleep(2)
        api_client.patch(f"/api/species/{species_id}/", {"name": "nombre actualizado"}, format="json")
        response = api_client.get(f"/api/species/{species_id}/")
        new_updated_at = response.data["updated_at"]
        assert new_updated_at > original_updated_at

    def test_update_species_invalid_status(self, created_species, api_client):
        response = api_client.patch(
            f"/api/species/{created_species['id']}/", {"status": "INVALID"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestDeleteSpecies:
    def test_delete_species_by_id_success(self, species_payload, api_client):
        create_resp = api_client.post("/api/species/", species_payload, format="json")
        species_id = create_resp.data["id"]

        delete_resp = api_client.delete(f"/api/species/{species_id}/")
        assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

        get_resp = api_client.get(f"/api/species/{species_id}/")
        assert get_resp.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_species_by_id_not_found(self, api_client):
        response = api_client.delete("/api/species/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_species_by_id_idempotent(self, species_payload, api_client):
        create_resp = api_client.post("/api/species/", species_payload, format="json")
        species_id = create_resp.data["id"]
        api_client.delete(f"/api/species/{species_id}/")
        second_delete = api_client.delete(f"/api/species/{species_id}/")
        assert second_delete.status_code == status.HTTP_404_NOT_FOUND

@pytest.fixture
def species_1(db):
    return Species.objects.create(name="hamster", status="active")

@pytest.fixture
def animal_1(db, species_1):
        return Animal.objects.create(name="orion", sex="male", species=species_1, adoption_status="available", medical_status="healthy")

class TestBusinessRules:
    def test_updated_species_with_status_blocked(self, api_client, species_1):
        update_payload = {"status": "inactive"}
        response = api_client.patch(f"/api/species/{species_1.id}/", update_payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
