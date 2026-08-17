from rest_framework import serializers

from vaccination_records.models import VaccinationRecord

from animals.models import Animal
from animals.serializers import AnimalShortSerializer

# serializer para leer los datos de un vaccination_record
class VaccinationRecordReadSerializer(serializers.ModelSerializer):
    animal = AnimalShortSerializer(read_only=True)
    class Meta:
        model = VaccinationRecord
        fields = ["id", "name", "animal", "status", "applied_at", "created_at", "updated_at"]
        # hacer que todos los campos sean de solo lectura
        read_only_fields = fields


# serializer para escribir los datos de un vaccination_record
class VaccinationRecordWriteSerializer(serializers.ModelSerializer):
    animal = serializers.PrimaryKeyRelatedField(queryset=Animal.objects.all())
    class Meta:
        model = VaccinationRecord
        fields = ["name", "animal", "status", "applied_at"]

    # sobrescribir el metodo to_representation para usar el serializer de lectura al devolver los datos
    def to_representation(self, instance: VaccinationRecord) -> dict:
        return VaccinationRecordReadSerializer(instance, context=self.context).data
