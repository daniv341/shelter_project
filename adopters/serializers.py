from rest_framework import serializers
from adopters.models import Adopter

# serializer para leer los datos de un adopter
class AdopterReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adopter
        fields = ["id", "full_name", "dni", "email", "phone", "status", "created_at", "updated_at"]
        # hacer que todos los campos sean de solo lectura
        read_only_fields = fields

class AdopterShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adopter
        fields = ["id", "full_name", "dni"]

# serializer para escribir los datos de un adopter
class AdopterWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adopter
        fields = ["full_name", "dni", "email", "phone", "status"]

    # sobrescribir el metodo to_representation para usar el serializer de lectura al devolver los datos
    def to_representation(self, instance: Adopter) -> dict:
        return AdopterReadSerializer(instance, context=self.context).data
