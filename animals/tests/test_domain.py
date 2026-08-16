"""
Pruebas de dominio: repository, selector y service, sin pasar por HTTP.
"""
from __future__ import annotations

import pytest
from django.http import Http404

from animals.models import Animal
from animals.repositories import AnimalRepository
from animals.selectors import AnimalSelector
from animals.services import AnimalService

pytestmark = pytest.mark.django_db


def make_animal_data(**overrides) -> dict:
    data = {
        "name": "Firulais",
        "species": "Perro",
        "sex": Animal.Sex.MALE,
        "adoption_status": Animal.AdoptionStatus.AVAILABLE,
        "medical_status": Animal.MedicalStatus.HEALTHY,
    }
    data.update(overrides)
    return data


class TestAnimalRepository:
    def test_create_persists_animal(self) -> None:
        repository = AnimalRepository()
        animal = repository.create(make_animal_data())

        assert animal.pk is not None
        assert Animal.objects.filter(pk=animal.pk).exists()
        assert len(animal.id) == 26  # longitud estándar de un ULID

    def test_update_modifies_fields(self) -> None:
        repository = AnimalRepository()
        animal = repository.create(make_animal_data())

        updated = repository.update(animal, {"name": "Nuevo Nombre"})

        animal.refresh_from_db()
        assert updated.name == "Nuevo Nombre"
        assert animal.name == "Nuevo Nombre"

    def test_delete_removes_animal(self) -> None:
        repository = AnimalRepository()
        animal = repository.create(make_animal_data())

        repository.delete(animal)

        assert not Animal.objects.filter(pk=animal.pk).exists()


class TestAnimalSelector:
    def test_get_all_returns_every_animal(self) -> None:
        selector = AnimalSelector()
        Animal.objects.create(**make_animal_data(name="A"))
        Animal.objects.create(**make_animal_data(name="B"))

        result = selector.get_all()

        assert result.count() == 2

    def test_get_by_id_returns_matching_animal(self) -> None:
        selector = AnimalSelector()
        animal = Animal.objects.create(**make_animal_data())

        result = selector.get_by_id(animal.pk)

        assert result.pk == animal.pk

    def test_get_by_id_raises_404_when_missing(self) -> None:
        selector = AnimalSelector()

        with pytest.raises(Http404):
            selector.get_by_id("01ARZ3NDEKTSV4RRFFQ69G5FAV")


class TestAnimalService:
    def test_create_animal_delegates_to_repository(self) -> None:
        service = AnimalService()

        animal = service.create_animal(make_animal_data(name="Michi"))

        assert animal.name == "Michi"
        assert Animal.objects.filter(pk=animal.pk).exists()

    def test_update_animal_finds_and_updates(self) -> None:
        service = AnimalService()
        animal = service.create_animal(make_animal_data())

        updated = service.update_animal(animal.pk, {"adoption_status": Animal.AdoptionStatus.ADOPTED})

        assert updated.adoption_status == Animal.AdoptionStatus.ADOPTED

    def test_delete_animal_removes_it(self) -> None:
        service = AnimalService()
        animal = service.create_animal(make_animal_data())

        service.delete_animal(animal.pk)

        assert not Animal.objects.filter(pk=animal.pk).exists()

    def test_list_animals_returns_queryset(self) -> None:
        service = AnimalService()
        service.create_animal(make_animal_data(name="A"))
        service.create_animal(make_animal_data(name="B"))

        result = service.list_animals()

        assert result.count() == 2
