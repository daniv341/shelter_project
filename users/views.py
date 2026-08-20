from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from users.filters import UserFilter
from users.serializers import UserReadSerializer, UserRegisterSerializer, UserWriteSerializer
from users.services import UserService
from users.permissions import IsStaffOrReadOnly


@extend_schema(tags=["Users"])
@extend_schema_view(
    list=extend_schema(
        summary="Listar users",
        description="Devuelve la lista paginada de users.",
        parameters=[
            OpenApiParameter(
                name="status", description="Filtra por estado exacto.",
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Obtener un user",
        description="Devuelve el detalle de un user por su id (ULID).",
    ),
    create=extend_schema(
        summary="Registrar un user",
        description="Da de alta un nuevo user.",
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente un user",
        description="Actualiza uno o mas campos de un user existente.",
    ),
    update=extend_schema(
        summary="Actualizar un user",
        description="Actualiza todos los campos editables de un user existente.",
    ),
    destroy=extend_schema(
        summary="Eliminar un user",
        description="Elimina definitivamente un user.",
    ),
)
class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.service = UserService()

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsStaffOrReadOnly()]

    def get_queryset(self):
        return self.service.list_users()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return UserReadSerializer
        if self.action == "create":
            return UserRegisterSerializer
        return UserWriteSerializer

    def perform_create(self, serializer):
        serializer.instance = self.service.create_user(
            serializer.validated_data
        )

    def perform_update(self, serializer):
        serializer.instance = self.service.update_user(
            serializer.instance.id,
            serializer.validated_data,
        )

    def perform_destroy(self, instance):
        self.service.delete_user(instance.id)