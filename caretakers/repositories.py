from __future__ import annotations
from typing import Any
from caretakers.models import Caretaker


class CaretakerRepository:
    def create(self, data: dict[str, Any]) -> Caretaker:
        return Caretaker.objects.create(**data)

    def update(self, caretaker: Caretaker, data: dict[str, Any]) -> Caretaker:
        for field, value in data.items():
            setattr(caretaker, field, value)
        caretaker.save()
        return caretaker

    def delete(self, caretaker: Caretaker) -> None:
        caretaker.delete()