from __future__ import annotations
import random
import time
import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from animals.models import Animal
from species.models import Species

pytestmark = pytest.mark.django_db

# funcion que crea las species necesarias para probar animals
@pytest.fixture
def species_list(db):
    return [
        Species.objects.create(name="perro", status="active"),
        Species.objects.create(name="gato", status="active"),
        Species.objects.create(name="conejo", status="active"),
    ]

@pytest.fixture
def api_client() -> APIClient:
    return APIClient()

@pytest.fixture
def make_payload(species_list):
    def _make_payload(**overrides):
        """Payload mínimo válido para crear un animal."""
        species = random.choice(species_list)
        payload = {
            "name": "jasmin",
            "species": species.id,
            "sex": Animal.Sex.MALE,
            "birth_date": "2002-08-17T19:16:27.889625",
            "admission_date": "2026-08-17T19:16:27.889625",
            "adoption_status": Animal.AdoptionStatus.AVAILABLE,
            "medical_status": Animal.MedicalStatus.HEALTHY,
            "description": "description de prueba",
        }
        payload.update(overrides)
        return payload

    return _make_payload

@pytest.fixture
def make_optional_only_payload(species_list):
    def _make_optional_only_payload(**overrides) -> dict:
        """Payload solo con los campos requeridos, sin los opcionales."""
        species = random.choice(species_list)
        payload = {
            "name": "jasmin",
            "species": species.id,
            "sex": Animal.Sex.MALE,
            "adoption_status": Animal.AdoptionStatus.AVAILABLE,
            "medical_status": Animal.MedicalStatus.HEALTHY,
        }
        payload.update(overrides)
        return payload
    return _make_optional_only_payload

@pytest.fixture
def animal_payload(make_payload) -> dict:
    return make_payload()

@pytest.fixture
def animal_optional_payload(make_optional_only_payload) -> dict:
    return make_optional_only_payload()


@pytest.fixture
def created_animal(animal_payload, api_client) -> dict:
    response = api_client.post("/api/animals/", animal_payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED, f"Setup fallo: {response.data}"
    return response.data


class TestCreateAnimal:
    def test_create_animal_success(self, animal_payload, api_client):
        response = api_client.post("/api/animals/", animal_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["name"] == animal_payload["name"]
        assert data["adoption_status"] == Animal.AdoptionStatus.AVAILABLE
        assert "id" in data

    def test_create_animal_without_optional_fields(self, animal_optional_payload, api_client):
        response = api_client.post("/api/animals/", animal_optional_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["adoption_status"] == Animal.AdoptionStatus.AVAILABLE
        assert data["name"] == animal_optional_payload["name"]

    def test_create_animal_missing_required_field(self, animal_payload, api_client):
        payload = animal_payload.copy()
        del payload["name"]
        response = api_client.post("/api/animals/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_animal_empty_required_field(self, animal_payload, api_client):
        payload = {**animal_payload, "name": ""}
        response = api_client.post("/api/animals/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_animal_with_invalid_date(
        self, make_payload, api_client) -> None:
        payload = make_payload(birth_date="17-08-2026 19:16:27")
        response = api_client.post("/api/animals/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_animal_returns_timestamps(self, animal_optional_payload,  api_client):
        response = api_client.post("/api/animals/", animal_optional_payload, format="json")
        data = response.data
        assert "created_at" in data
        assert "updated_at" in data


class TestGetAllAnimals:
    def test_get_all_returns_paginated_list(self, api_client):
        response = api_client.get("/api/animals/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_get_all_contains_created_animal(self, created_animal, api_client):
        response = api_client.get("/api/animals/")
        results = response.data["results"]
        ids = [item["id"] for item in results]
        assert created_animal["id"] in ids

    def test_get_all_animal_fields(self, created_animal, api_client):
        response = api_client.get("/api/animals/")
        results = response.data["results"]
        item = next((p for p in results if p["id"] == created_animal["id"]), None)
        assert item is not None
        for field in ("name", "id", "species", "sex"):
            assert field in item

    def test_get_all_filtering_by_status(self, created_animal, api_client):
        params = {"adoption_status": Animal.AdoptionStatus.AVAILABLE}
        response = api_client.get("/api/animals/", params)
        results = response.data["results"]
        assert len(results) > 0
        for item in results:
            assert item["adoption_status"] == Animal.AdoptionStatus.AVAILABLE


class TestGetAnimalById:
    def test_get_animal_by_id_success(self, created_animal, api_client):
        animal_id = created_animal["id"]
        response = api_client.get(f"/api/animals/{animal_id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == animal_id

    def test_get_animal_by_id_not_found(self, api_client):
        response = api_client.get("/api/animals/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_animal_by_id_returns_correct_data(self, created_animal, api_client):
        response = api_client.get(f"/api/animals/{created_animal['id']}/")
        data = response.data
        assert data["name"] == created_animal["name"]


class TestUpdateAnimal:
    def test_update_animal_by_id_success(self, created_animal, api_client):
        animal_id = created_animal["id"]
        update_payload = {"adoption_status": Animal.AdoptionStatus.ADOPTED}
        response = api_client.patch(f"/api/animals/{animal_id}/", update_payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data["adoption_status"] == Animal.AdoptionStatus.ADOPTED

    def test_update_animal_by_id_not_found(self, api_client):
        response = api_client.patch(
            "/api/animals/01ARZ3NDEKTSV4RRFFQ69G5FAV/",
            {"adoption_status": Animal.AdoptionStatus.ADOPTED},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_animal_updates_updated_at(self, created_animal, api_client):
        animal_id = created_animal["id"]
        original_updated_at = created_animal["updated_at"]
        time.sleep(2)
        api_client.patch(f"/api/animals/{animal_id}/", {"name": "nuevo nombre"}, format="json")
        response = api_client.get(f"/api/animals/{animal_id}/")
        new_updated_at = response.data["updated_at"]
        assert new_updated_at > original_updated_at

    def test_update_animal_invalid_status(self, created_animal, api_client):
        response = api_client.patch(
            f"/api/animals/{created_animal['id']}/", {"adoption_status": "INVALID"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestDeleteAnimal:
    def test_delete_animal_by_id_success(self, animal_payload, api_client):
        create_resp = api_client.post("/api/animals/", animal_payload, format="json")
        animal_id = create_resp.data["id"]

        delete_resp = api_client.delete(f"/api/animals/{animal_id}/")
        assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

        get_resp = api_client.get(f"/api/animals/{animal_id}/")
        assert get_resp.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_animal_by_id_not_found(self, api_client):
        response = api_client.delete("/api/animals/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_animal_by_id_idempotent(self, animal_payload, api_client):
        create_resp = api_client.post("/api/animals/", animal_payload, format="json")
        animal_id = create_resp.data["id"]
        api_client.delete(f"/api/animals/{animal_id}/")
        second_delete = api_client.delete(f"/api/animals/{animal_id}/")
        assert second_delete.status_code == status.HTTP_404_NOT_FOUND
