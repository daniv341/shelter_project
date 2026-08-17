"""
filters.py

Filtros para el endpoint de listado de animales, basados en
django-filter e integrados vía DjangoFilterBackend (DRF).
"""
from __future__ import annotations

import django_filters

from animals.models import Animal


class AnimalFilter(django_filters.FilterSet):
    species = django_filters.CharFilter(field_name="species_id")

    class Meta:
        model = Animal
        fields = ["species", "sex", "adoption_status", "medical_status"]
