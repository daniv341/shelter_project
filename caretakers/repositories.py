from __future__ import annotations
from typing import Any
from caretakers.models import Caretaker


class CaretakerRepository:
    # crear un caretaker
    def create(self, data: dict[str, Any]) -> Caretaker:
        # retorna el caretaker, **data desempaqueta los datos y los pasa como argumentos
        return Caretaker.objects.create(**data)

    # actualizar un caretaker
    def update(self, caretaker: Caretaker, data: dict[str, Any]) -> Caretaker:
        # actualizar los campos del caretaker con los datos proporcionados
        for field, value in data.items():
            setattr(caretaker, field, value)
        caretaker.save()
        return caretaker

    # eliminar un caretaker
    def delete(self, caretaker: Caretaker) -> None:
        caretaker.delete()