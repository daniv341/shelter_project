from rest_framework import serializers
from adoption_events.models import AdoptionEvent

from animals.models import Animal
from adopters.models import Adopter
from adoption_applications.models import AdoptionApplication
from animals.serializers import AnimalShortSerializer
from adopters.serializers import AdopterShortSerializer
from adoption_applications.serializers import AdoptionApplicationShoirtSerializer

# serializer para leer los datos de un adoption_event
class AdoptionEventReadSerializer(serializers.ModelSerializer):
    animal = AnimalShortSerializer(read_only=True)
    adopter = AdopterShortSerializer(read_only=True)
    adoption_application = AdoptionApplicationShoirtSerializer(read_only=True)
    class Meta:
        model = AdoptionEvent
        fields = ["id", "animal", "adopter", "status", "adoption_application", "adopted_at", "notes", "created_at", "updated_at"]
        # hacer que todos los campos sean de solo lectura
        read_only_fields = fields


# serializer para escribir los datos de un adoption_event
class AdoptionEventWriteSerializer(serializers.ModelSerializer):
    animal = serializers.PrimaryKeyRelatedField(queryset=Animal.objects.all())
    adopter = serializers.PrimaryKeyRelatedField(queryset=Adopter.objects.all())
    adoption_application = serializers.PrimaryKeyRelatedField(queryset=AdoptionApplication.objects.all())
    class Meta:
        model = AdoptionEvent
        fields = ["animal", "adopter", "status", "adoption_application", "adopted_at", "notes"]

    # sobrescribir el metodo to_representation para usar el serializer de lectura al devolver los datos
    def to_representation(self, instance: AdoptionEvent) -> dict:
        return AdoptionEventReadSerializer(instance, context=self.context).data
