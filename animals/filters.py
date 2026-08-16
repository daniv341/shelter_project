"""
filters.py

Filtros para el endpoint de listado de animales, basados en
django-filter e integrados vía DjangoFilterBackend (DRF).
"""
from __future__ import annotations

import django_filters

from animals.models import Animal


class AnimalFilter(django_filters.FilterSet):
    species = django_filters.CharFilter(field_name="species", lookup_expr="icontains")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Animal
        fields = ["species", "name", "sex", "adoption_status", "medical_status"]
