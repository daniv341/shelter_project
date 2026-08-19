from rest_framework import serializers
from caretaker_assignments.models import CaretakerAssignment

from animals.models import Animal
from caretakers.models import Caretaker
from animals.serializers import AnimalShortSerializer
from caretakers.serializers import CaretakerShortSerializer

# serializer para leer los datos de un caretaker_assignment
class CaretakerAssignmentReadSerializer(serializers.ModelSerializer):
    animal = AnimalShortSerializer(read_only=True)
    caretaker = CaretakerShortSerializer(read_only=True)
    class Meta:
        model = CaretakerAssignment
        fields = ["id", "animal", "caretaker", "status", "assignment_at", "notes", "created_at", "updated_at"]
        # hacer que todos los campos sean de solo lectura
        read_only_fields = fields


# serializer para escribir los datos de un caretaker_assignment
class CaretakerAssignmentWriteSerializer(serializers.ModelSerializer):
    animal = serializers.PrimaryKeyRelatedField(queryset=Animal.objects.all())
    caretaker = serializers.PrimaryKeyRelatedField(queryset=Caretaker.objects.all())
    class Meta:
        model = CaretakerAssignment
        fields = ["animal", "caretaker", "status", "assignment_at", "notes"]

    # sobrescribir el metodo to_representation para usar el serializer de lectura al devolver los datos
    def to_representation(self, instance: CaretakerAssignment) -> dict:
        return CaretakerAssignmentReadSerializer(instance, context=self.context).data
