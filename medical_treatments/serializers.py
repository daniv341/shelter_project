from rest_framework import serializers

from medical_treatments.models import MedicalTreatment

from animals.models import Animal
from veterinarians.models import Veterinarian
from animals.serializers import AnimalShortSerializer
from veterinarians.serializers import VeterinarianShortSerializer

# serializer para leer los datos de un medical_treatment
class MedicalTreatmentReadSerializer(serializers.ModelSerializer):
    animal = AnimalShortSerializer(read_only=True)
    veterinarian = VeterinarianShortSerializer(read_only=True)
    class Meta:
        model = MedicalTreatment
        fields = ["id", "diagnostic", "animal", "veterinarian", "status", "description", "started_at", "ended_at", "created_at", "updated_at"]
        # hacer que todos los campos sean de solo lectura
        read_only_fields = fields


# serializer para escribir los datos de un medical_treatment
class MedicalTreatmentWriteSerializer(serializers.ModelSerializer):
    animal = serializers.PrimaryKeyRelatedField(queryset=Animal.objects.all())
    veterinarian = serializers.PrimaryKeyRelatedField(queryset=Veterinarian.objects.all())
    class Meta:
        model = MedicalTreatment
        fields = ["diagnostic", "animal", "veterinarian", "status", "description", "started_at", "ended_at"]

    # sobrescribir el metodo to_representation para usar el serializer de lectura al devolver los datos
    def to_representation(self, instance: MedicalTreatment) -> dict:
        return MedicalTreatmentReadSerializer(instance, context=self.context).data
