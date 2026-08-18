from rest_framework import serializers
from adoption_applications.models import AdoptionApplication

from animals.models import Animal
from adopters.models import Adopter
from animals.serializers import AnimalShortSerializer
from adopters.serializers import AdopterShortSerializer

# serializer para leer los datos de un adoption_application
class AdoptionApplicationReadSerializer(serializers.ModelSerializer):
    animal = AnimalShortSerializer(read_only=True)
    adopter = AdopterShortSerializer(read_only=True)
    class Meta:
        model = AdoptionApplication
        fields = ["id", "animal", "adopter", "status", "submitted_at", "reviewed_at", "notes", "created_at", "updated_at"]
        # hacer que todos los campos sean de solo lectura
        read_only_fields = fields


# serializer para escribir los datos de un adoption_application
class AdoptionApplicationWriteSerializer(serializers.ModelSerializer):
    animal = serializers.PrimaryKeyRelatedField(queryset=Animal.objects.all())
    adopter = serializers.PrimaryKeyRelatedField(queryset=Adopter.objects.all())
    class Meta:
        model = AdoptionApplication
        fields = ["animal", "adopter", "status", "submitted_at", "reviewed_at", "notes"]

    # sobrescribir el metodo to_representation para usar el serializer de lectura al devolver los datos
    def to_representation(self, instance: AdoptionApplication) -> dict:
        return AdoptionApplicationReadSerializer(instance, context=self.context).data
