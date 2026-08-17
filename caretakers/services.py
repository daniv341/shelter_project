from __future__ import annotations
from typing import Any
from caretakers.repositories import CaretakerRepository
from caretakers.selectors import CaretakerSelector


class CaretakerService:
    # inicializar el servicio con un repositorio y un selector opcionales, son opcionales para permitir las dependecias y facilitar las pruebas
    def __init__(self, repository: CaretakerRepository | None = None, selector: CaretakerSelector | None = None) -> None:
        self.repository = repository or CaretakerRepository()
        self.selector = selector or CaretakerSelector()

    # listar todos los caretakers
    def list_caretakers(self):
        return self.selector.get_all()
    
    # obtener un caretaker por su id
    def get_caretaker(self, caretaker_id: str):
        return self.selector.get_by_id(caretaker_id)

    # crear un caretaker
    def create_caretaker(self, data: dict[str, Any]):
        return self.repository.create(data)

    # actualizar un caretaker
    def update_caretaker(self, caretaker_id: str, data: dict[str, Any]):
        caretaker = self.selector.get_by_id(caretaker_id)
        return self.repository.update(caretaker, data)

    # eliminar un caretaker
    def delete_caretaker(self, caretaker_id: str) -> None:
        caretaker = self.selector.get_by_id(caretaker_id)
        self.repository.delete(caretaker)