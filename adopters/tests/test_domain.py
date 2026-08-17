from __future__ import annotations

import pytest
from django.http import Http404
import uuid

from adopters.models import Adopter
from adopters.repositories import AdopterRepository
from adopters.selectors import AdopterSelector
from adopters.services import AdopterService

pytestmark = pytest.mark.django_db


def make_adopter_data(**overrides) -> dict:
    data = {
        "full_name": "nombre de prueba",
        "dni": f"{uuid.uuid4().int % 10000000}",
        "email": f"test_{uuid.uuid4().hex[:5]}@gmail.com",
        "phone": "381123456",
        "status": Adopter.Status.ACTIVE,
    }
    data.update(overrides)
    return data


class TestAdopterRepository:
    def test_create_persists_adopter(self) -> None:
        repository = AdopterRepository()
        adopter = repository.create(make_adopter_data())

        assert adopter.pk is not None
        assert Adopter.objects.filter(pk=adopter.pk).exists()
        assert len(adopter.id) == 26  # longitud estandar de un ULID

    def test_update_modifies_fields(self) -> None:
        repository = AdopterRepository()
        adopter = repository.create(make_adopter_data())

        updated = repository.update(adopter, {"full_name": "nuevo nombre"})

        adopter.refresh_from_db()
        assert updated.full_name == "nuevo nombre"
        assert adopter.full_name == "nuevo nombre"

    def test_delete_removes_adopter(self) -> None:
        repository = AdopterRepository()
        adopter = repository.create(make_adopter_data())

        repository.delete(adopter)

        assert not Adopter.objects.filter(pk=adopter.pk).exists()


class TestAdopterSelector:
    def test_get_all_returns_every_adopter(self) -> None:
        selector = AdopterSelector()
        Adopter.objects.create(**make_adopter_data())
        Adopter.objects.create(**make_adopter_data())

        result = selector.get_all()

        assert result.count() == 2

    def test_get_by_id_returns_matching_adopter(self) -> None:
        selector = AdopterSelector()
        adopter = Adopter.objects.create(**make_adopter_data())

        result = selector.get_by_id(adopter.pk)

        assert result.pk == adopter.pk

    def test_get_by_id_raises_404_when_missing(self) -> None:
        selector = AdopterSelector()

        with pytest.raises(Http404):
            selector.get_by_id("01ARZ3NDEKTSV4RRFFQ69G5FAV")


class TestAdopterService:
    def test_create_adopter_delegates_to_repository(self) -> None:
        service = AdopterService()

        adopter = service.create_adopter(make_adopter_data())

        assert Adopter.objects.filter(pk=adopter.pk).exists()

    def test_update_adopter_finds_and_updates(self) -> None:
        service = AdopterService()
        adopter = service.create_adopter(make_adopter_data())

        updated = service.update_adopter(adopter.pk, {"status": Adopter.Status.BLOCKED})

        assert updated.status == Adopter.Status.BLOCKED

    def test_delete_adopter_removes_it(self) -> None:
        service = AdopterService()
        adopter = service.create_adopter(make_adopter_data())

        service.delete_adopter(adopter.pk)

        assert not Adopter.objects.filter(pk=adopter.pk).exists()

    def test_list_adopters_returns_queryset(self) -> None:
        service = AdopterService()
        service.create_adopter(make_adopter_data())
        service.create_adopter(make_adopter_data())

        result = service.list_adopters()

        assert result.count() == 2
