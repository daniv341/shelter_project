"""
Pruebas de los endpoints REST del módulo animals.
"""
from __future__ import annotations

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from animals.models import Animal

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


def make_payload(**overrides) -> dict:
    payload = {
        "name": "Firulais",
        "species": "Perro",
        "sex": Animal.Sex.MALE,
        "adoption_status": Animal.AdoptionStatus.AVAILABLE,
        "medical_status": Animal.MedicalStatus.HEALTHY,
    }
    payload.update(overrides)
    return payload


class TestListAnimals:
    def test_returns_paginated_list(self, api_client: APIClient) -> None:
        Animal.objects.create(**{**make_payload(), "name": "A"})
        Animal.objects.create(**{**make_payload(), "name": "B"})

        response = api_client.get("/api/animals/")
        print(response)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

    def test_filters_by_species(self, api_client: APIClient) -> None:
        Animal.objects.create(**{**make_payload(), "species": "Perro"})
        Animal.objects.create(**{**make_payload(), "species": "Gato"})

        response = api_client.get("/api/animals/", {"species": "gato"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["species"] == "Gato"


class TestRetrieveAnimal:
    def test_returns_animal_detail(self, api_client: APIClient) -> None:
        animal = Animal.objects.create(**make_payload())

        response = api_client.get(f"/api/animals/{animal.pk}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == animal.pk

    def test_returns_404_when_not_found(self, api_client: APIClient) -> None:
        response = api_client.get("/api/animals/01ARZ3NDEKTSV4RRFFQ69G5FAV/")

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestCreateAnimal:
    def test_creates_animal_with_valid_payload(self, api_client: APIClient) -> None:
        response = api_client.post("/api/animals/", make_payload(), format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Firulais"
        assert Animal.objects.count() == 1

    def test_returns_400_with_invalid_payload(self, api_client: APIClient) -> None:
        payload = make_payload()
        payload.pop("name")

        response = api_client.post("/api/animals/", payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestUpdateAnimal:
    def test_partial_update_modifies_field(self, api_client: APIClient) -> None:
        animal = Animal.objects.create(**make_payload())

        response = api_client.patch(
            f"/api/animals/{animal.pk}/",
            {"adoption_status": Animal.AdoptionStatus.ADOPTED},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        animal.refresh_from_db()
        assert animal.adoption_status == Animal.AdoptionStatus.ADOPTED


class TestDeleteAnimal:
    def test_deletes_existing_animal(self, api_client: APIClient) -> None:
        animal = Animal.objects.create(**make_payload())

        response = api_client.delete(f"/api/animals/{animal.pk}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Animal.objects.filter(pk=animal.pk).exists()
