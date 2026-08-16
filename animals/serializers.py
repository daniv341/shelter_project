"""
serializers.py

Validación y serialización de datos de entrada (write) y salida (read).

Se usan dos serializers separados:
- AnimalReadSerializer: representación completa de salida (incluye id,
  timestamps y foto).
- AnimalWriteSerializer: validación de entrada para create/update. No
  incluye "photo" porque la API fuerza application/json como
  content-type por defecto (ver REST_FRAMEWORK.DEFAULT_PARSER_CLASSES
  en settings.py); la carga de archivos quedará como una extensión
  futura con un endpoint/parser dedicado a multipart.
"""
from __future__ import annotations

from rest_framework import serializers

from animals.models import Animal


class AnimalReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = [
            "id",
            "name",
            "species",
            "sex",
            "birth_date",
            "admission_date",
            "adoption_status",
            "medical_status",
            "description",
            "photo",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class AnimalWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = [
            "name",
            "species",
            "sex",
            "birth_date",
            "admission_date",
            "adoption_status",
            "medical_status",
            "description",
        ]

    def to_representation(self, instance: Animal) -> dict:
        # Al finalizar un create/update, se responde con la
        # representación completa de lectura (incluye id, timestamps, etc.)
        return AnimalReadSerializer(instance, context=self.context).data
