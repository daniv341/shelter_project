from rest_framework import serializers
from veterinarians.models import Veterinatian

# serializer para leer los datos de un veterinatian
class VeterinatianReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veterinatian
        fields = ["id", "name", "status", "created_at", "updated_at"]
        # hacer que todos los campos sean de solo lectura
        read_only_fields = fields


# serializer para escribir los datos de un veterinatian
class VeterinatianWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veterinatian
        fields = ["name", "status"]

    # sobrescribir el metodo to_representation para usar el serializer de lectura al devolver los datos
    def to_representation(self, instance: Veterinatian) -> dict:
        return VeterinatianReadSerializer(instance, context=self.context).data
