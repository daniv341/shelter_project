from __future__ import annotations

from rest_framework import serializers

from animals.models import Animal
from species.models import Species
from species.serializers import SpeciesShortSerializer


class AnimalReadSerializer(serializers.ModelSerializer):
    # hace que species sea el serializers short que creaste en species
    species = SpeciesShortSerializer(read_only=True)
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
    # esta linea hace que species deba ser el atributo primario(id) del objeto Species
    species = serializers.PrimaryKeyRelatedField(queryset=Species.objects.all())

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
