from rest_framework import serializers
from species.models import Species

# serializer para leer los datos de un species
class SpeciesReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ["id", "name", "status", "created_at", "updated_at"]
        # hacer que todos los campos sean de solo lectura
        read_only_fields = fields

# serializers de lectura que se puede usar en otros objetos que dependan de species
class SpeciesShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ["id", "name"]

# serializer para escribir los datos de un species
class SpeciesWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ["name", "status"]

    # sobrescribir el metodo to_representation para usar el serializer de lectura al devolver los datos
    def to_representation(self, instance: Species) -> dict:
        return SpeciesReadSerializer(instance, context=self.context).data
