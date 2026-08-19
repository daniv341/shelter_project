from rest_framework import serializers
from donations.models import Donation

from adopters.models import Adopter
from adopters.serializers import AdopterShortSerializer

# serializer para leer los datos de un donation
class DonationReadSerializer(serializers.ModelSerializer):
    adopter = AdopterShortSerializer(read_only=True)
    class Meta:
        model = Donation
        fields = ["id", "adopter", "mount", "type_donation", "status", "donated_at", "created_at", "updated_at"]
        # hacer que todos los campos sean de solo lectura
        read_only_fields = fields


# serializer para escribir los datos de un donation
class DonationWriteSerializer(serializers.ModelSerializer):
    # dado que el adopter puede ser null o opcional, debes agregar esos campos de lo contrario los tomara como obligatorios
    adopter = serializers.PrimaryKeyRelatedField(queryset=Adopter.objects.all(), required=False, allow_null=True)
    class Meta:
        model = Donation
        fields = ["adopter", "mount", "type_donation", "status", "donated_at"]

    # sobrescribir el metodo to_representation para usar el serializer de lectura al devolver los datos
    def to_representation(self, instance: Donation) -> dict:
        return DonationReadSerializer(instance, context=self.context).data
