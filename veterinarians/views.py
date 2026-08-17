from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema_view, extend_schema
from rest_framework import mixins, viewsets

from veterinarians.filters import VeterinatianFilter
from veterinarians.serializers import VeterinatianReadSerializer, VeterinatianWriteSerializer
from veterinarians.services import VeterinatianService

@extend_schema(tags=["Veterinarians"])
@extend_schema_view(
    list=extend_schema(
        summary="Listar veterinarians",
        description="Devuelve la lista paginada de veterinarians.",
        parameters=[
            OpenApiParameter(name="status", description="Filtra por estado exacto."),
        ],
    ),
    retrieve=extend_schema(
        summary="Obtener un veterinatian",
        description="Devuelve el detalle de un veterinatian por su id (ULID).",
    ),
    create=extend_schema(
        summary="Registrar un veterinatian",
        description="Da de alta un nuevo veterinatian.",
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente un veterinatian",
        description="Actualiza uno o mas campos de un veterinatian existente.",
    ),
    update=extend_schema(
        summary="Actualizar un veterinatian",
        description="Actualiza todos los campos editables de un veterinatian existente.",
    ),
    destroy=extend_schema(
        summary="Eliminar un veterinatian",
        description="Elimina definitivamente un veterinatian.",
    ),
)
class VeterinatianViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,
):
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend]
    filterset_class = VeterinatianFilter

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.service = VeterinatianService()

    def get_queryset(self):
        return self.service.list_veterinarians()

    def get_serializer_class(self):
        return VeterinatianReadSerializer if self.action in ("list", "retrieve") else VeterinatianWriteSerializer

    def perform_create(self, serializer):
        serializer.instance = self.service.create_veterinatian(serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = self.service.update_veterinatian(serializer.instance.id, serializer.validated_data)

    def perform_destroy(self, instance):
        self.service.delete_veterinatian(instance.id)
