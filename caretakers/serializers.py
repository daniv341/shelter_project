from rest_framework import serializers
from caretakers.models import Caretaker


class CaretakerReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caretaker
        fields = ["id", "full_name", "dni", "email", "phone", "status", "created_at", "updated_at"]
        read_only_fields = fields


class CaretakerWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caretaker
        fields = ["full_name", "dni", "email", "phone", "status"]

    def to_representation(self, instance: Caretaker) -> dict:
        return CaretakerReadSerializer(instance, context=self.context).data