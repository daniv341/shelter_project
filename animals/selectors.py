"""
selectors.py

Encapsula las consultas de lectura (queries) sobre el modelo Animal.
Separar los selectors de los repositories permite optimizar lecturas
(select_related, prefetch, anotaciones, etc.) sin mezclar esa
responsabilidad con las operaciones de escritura.
"""
from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from animals.models import Animal


class AnimalSelector:
    """Operaciones de lectura sobre Animal."""

    def get_by_id(self, animal_id: str) -> Animal:
        return get_object_or_404(Animal, pk=animal_id)

    def get_all(self) -> QuerySet[Animal]:
        # retorna todos los animales, con species ya cargado para evitar N+1 queries
        return Animal.objects.select_related("species")
