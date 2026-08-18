from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema_view, extend_schema
from rest_framework import mixins, viewsets

from veterinarians.filters import VeterinarianFilter
from veterinarians.serializers import VeterinarianReadSerializer, VeterinarianWriteSerializer
from veterinarians.services import VeterinarianService

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
        summary="Obtener un veterinarian",
        description="Devuelve el detalle de un veterinarian por su id (ULID).",
    ),
    create=extend_schema(
        summary="Registrar un veterinarian",
        description="Da de alta un nuevo veterinarian.",
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente un veterinarian",
        description="Actualiza uno o mas campos de un veterinarian existente.",
    ),
    update=extend_schema(
        summary="Actualizar un veterinarian",
        description="Actualiza todos los campos editables de un veterinarian existente.",
    ),
    destroy=extend_schema(
        summary="Eliminar un veterinarian",
        description="Elimina definitivamente un veterinarian.",
    ),
)
class VeterinarianViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,
):
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend]
    filterset_class = VeterinarianFilter

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.service = VeterinarianService()

    def get_queryset(self):
        return self.service.list_veterinarians()

    def get_serializer_class(self):
        return VeterinarianReadSerializer if self.action in ("list", "retrieve") else VeterinarianWriteSerializer

    def perform_create(self, serializer):
        serializer.instance = self.service.create_veterinarian(serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = self.service.update_veterinarian(serializer.instance.id, serializer.validated_data)

    def perform_destroy(self, instance):
        self.service.delete_veterinarian(instance.id)
