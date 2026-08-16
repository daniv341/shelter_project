from __future__ import annotations

import pytest
from django.http import Http404
import uuid

from caretakers.models import Caretaker
from caretakers.repositories import CaretakerRepository
from caretakers.selectors import CaretakerSelector
from caretakers.services import CaretakerService

pytestmark = pytest.mark.django_db


def make_caretaker_data(**overrides) -> dict:
    data = {
        "full_name": "Micaela Rodriguez",
        "dni": f"{uuid.uuid4().int % 10000000}",
        "email": f"test_{uuid.uuid4().hex[:5]}@gmail.com",
        "phone": "381123456",
        "status": Caretaker.Status.ACTIVE,
    }
    data.update(overrides)
    return data


class TestCaretakerRepository:
    def test_create_persists_caretaker(self) -> None:
        repository = CaretakerRepository()
        caretaker = repository.create(make_caretaker_data())

        assert caretaker.pk is not None
        assert Caretaker.objects.filter(pk=caretaker.pk).exists()
        assert len(caretaker.id) == 26  # longitud estándar de un ULID

    def test_update_modifies_fields(self) -> None:
        repository = CaretakerRepository()
        caretaker = repository.create(make_caretaker_data())

        updated = repository.update(caretaker, {"full_name": "Nuevo Nombre"})

        caretaker.refresh_from_db()
        assert updated.full_name == "Nuevo Nombre"
        assert caretaker.full_name == "Nuevo Nombre"

    def test_delete_removes_caretaker(self) -> None:
        repository = CaretakerRepository()
        caretaker = repository.create(make_caretaker_data())

        repository.delete(caretaker)

        assert not Caretaker.objects.filter(pk=caretaker.pk).exists()


class TestCaretakerSelector:
    def test_get_all_returns_every_caretaker(self) -> None:
        selector = CaretakerSelector()
        Caretaker.objects.create(**make_caretaker_data(full_name="A"))
        Caretaker.objects.create(**make_caretaker_data(full_name="B"))

        result = selector.get_all()

        assert result.count() == 2

    def test_get_by_id_returns_matching_caretaker(self) -> None:
        selector = CaretakerSelector()
        caretaker = Caretaker.objects.create(**make_caretaker_data())

        result = selector.get_by_id(caretaker.pk)

        assert result.pk == caretaker.pk

    def test_get_by_id_raises_404_when_missing(self) -> None:
        selector = CaretakerSelector()

        with pytest.raises(Http404):
            selector.get_by_id("01ARZ3NDEKTSV4RRFFQ69G5FAV")


class TestCaretakerService:
    def test_create_caretaker_delegates_to_repository(self) -> None:
        service = CaretakerService()

        caretaker = service.create_caretaker(make_caretaker_data(full_name="Prueba"))

        assert caretaker.full_name == "Prueba"
        assert Caretaker.objects.filter(pk=caretaker.pk).exists()

    def test_update_caretaker_finds_and_updates(self) -> None:
        service = CaretakerService()
        caretaker = service.create_caretaker(make_caretaker_data())

        updated = service.update_caretaker(caretaker.pk, {"status": Caretaker.Status.BLOCKED})

        assert updated.status == Caretaker.Status.BLOCKED

    def test_delete_caretaker_removes_it(self) -> None:
        service = CaretakerService()
        caretaker = service.create_caretaker(make_caretaker_data())

        service.delete_caretaker(caretaker.pk)

        assert not Caretaker.objects.filter(pk=caretaker.pk).exists()

    def test_list_caretakers_returns_queryset(self) -> None:
        service = CaretakerService()
        service.create_caretaker(make_caretaker_data(full_name="A"))
        service.create_caretaker(make_caretaker_data(full_name="B"))

        result = service.list_caretakers()

        assert result.count() == 2

