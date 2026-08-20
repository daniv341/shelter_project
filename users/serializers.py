from rest_framework import serializers
from users.models import User

# serializer para leer los datos de un user
class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "user_name", "email", "status", "created_at", "updated_at", "is_staff", "is_superuser"]
        # hacer que todos los campos sean de solo lectura
        read_only_fields = fields


# serializer para escribir los datos de un user
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ["user_name", "email", "password"]

    # sobrescribir el metodo to_representation para usar el serializer de lectura al devolver los datos
    def to_representation(self, instance: User) -> dict:
        return UserReadSerializer(instance, context=self.context).data

# serializer para escribir los datos de un user
class UserWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=False)
    class Meta:
        model = User
        fields = ["user_name", "email", "password", "status"]
    # sobrescribir el metodo to_representation para usar el serializer de lectura al devolver los datos
    def to_representation(self, instance: User) -> dict:
        return UserReadSerializer(instance, context=self.context).data
