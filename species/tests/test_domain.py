from __future__ import annotations

import pytest
from django.http import Http404
import uuid

from species.models import Species
from species.repositories import SpeciesRepository
from species.selectors import SpeciesSelector
from species.services import SpeciesService

pytestmark = pytest.mark.django_db


def make_species_data(**overrides) -> dict:
    data = {
        "name": "Texto de prueba",
    }
    data.update(overrides)
    return data


class TestSpeciesRepository:
    def test_create_persists_species(self) -> None:
        repository = SpeciesRepository()
        species = repository.create(make_species_data())

        assert species.pk is not None
        assert Species.objects.filter(pk=species.pk).exists()
        assert len(species.id) == 26  # longitud estandar de un ULID

    def test_update_modifies_fields(self) -> None:
        repository = SpeciesRepository()
        species = repository.create(make_species_data())

        updated = repository.update(species, {"name": "Nuevo valor"})

        species.refresh_from_db()
        assert updated.name == "Nuevo valor"
        assert species.name == "Nuevo valor"

    def test_delete_removes_species(self) -> None:
        repository = SpeciesRepository()
        species = repository.create(make_species_data())

        repository.delete(species)

        assert not Species.objects.filter(pk=species.pk).exists()


class TestSpeciesSelector:
    def test_get_all_returns_every_species(self) -> None:
        selector = SpeciesSelector()
        Species.objects.create(**make_species_data())
        Species.objects.create(**make_species_data())

        result = selector.get_all()

        assert result.count() == 2

    def test_get_by_id_returns_matching_species(self) -> None:
        selector = SpeciesSelector()
        species = Species.objects.create(**make_species_data())

        result = selector.get_by_id(species.pk)

        assert result.pk == species.pk

    def test_get_by_id_raises_404_when_missing(self) -> None:
        selector = SpeciesSelector()

        with pytest.raises(Http404):
            selector.get_by_id("01ARZ3NDEKTSV4RRFFQ69G5FAV")


class TestSpeciesService:
    def test_create_species_delegates_to_repository(self) -> None:
        service = SpeciesService()

        species = service.create_species(make_species_data())

        assert Species.objects.filter(pk=species.pk).exists()

    def test_update_species_finds_and_updates(self) -> None:
        service = SpeciesService()
        species = service.create_species(make_species_data())

        updated = service.update_species(species.pk, {"status": Species.Status.BLOCKED})

        assert updated.status == Species.Status.BLOCKED

    def test_delete_species_removes_it(self) -> None:
        service = SpeciesService()
        species = service.create_species(make_species_data())

        service.delete_species(species.pk)

        assert not Species.objects.filter(pk=species.pk).exists()

    def test_list_species_returns_queryset(self) -> None:
        service = SpeciesService()
        service.create_species(make_species_data())
        service.create_species(make_species_data())

        result = service.list_species()

        assert result.count() == 2
