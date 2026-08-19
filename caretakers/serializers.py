from rest_framework import serializers
from caretakers.models import Caretaker

#serializer para leer los datos de un caretaker
class CaretakerReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caretaker
        fields = ["id", "full_name", "dni", "email", "phone", "status", "created_at", "updated_at"]
        # hacer que todos los campos sean de solo lectura
        read_only_fields = fields

class CaretakerShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caretaker
        fields = ["id", "full_name", "dni"]

# serializer para escribir los datos de un caretaker
class CaretakerWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caretaker
        fields = ["full_name", "dni", "email", "phone", "status"]

    # sobrescribir el método to_representation para usar el serializer de lectura al devolver los datos
    def to_representation(self, instance: Caretaker) -> dict:
        return CaretakerReadSerializer(instance, context=self.context).data