from rest_framework import serializers
from veterinarians.models import Veterinarian

# serializer para leer los datos de un veterinarian
class VeterinarianReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veterinarian
        fields = ["id", "full_name", "dni", "email", "phone", "status", "created_at", "updated_at"]
        # hacer que todos los campos sean de solo lectura
        read_only_fields = fields

class VeterinarianShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veterinarian
        fields = ["id", "full_name"]

# serializer para escribir los datos de un veterinarian
class VeterinarianWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veterinarian
        fields = ["full_name", "dni", "email", "phone", "status"]

    # sobrescribir el metodo to_representation para usar el serializer de lectura al devolver los datos
    def to_representation(self, instance: Veterinarian) -> dict:
        return VeterinarianReadSerializer(instance, context=self.context).data
