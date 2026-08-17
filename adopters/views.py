from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema_view, extend_schema
from rest_framework import mixins, viewsets

from adopters.filters import AdopterFilter
from adopters.serializers import AdopterReadSerializer, AdopterWriteSerializer
from adopters.services import AdopterService

@extend_schema(tags=["Adopters"])
@extend_schema_view(
    list=extend_schema(
        summary="Listar adopters",
        description="Devuelve la lista paginada de adopters.",
        parameters=[
            OpenApiParameter(name="status", description="Filtra por estado exacto."),
        ],
    ),
    retrieve=extend_schema(
        summary="Obtener un adopter",
        description="Devuelve el detalle de un adopter por su id (ULID).",
    ),
    create=extend_schema(
        summary="Registrar un adopter",
        description="Da de alta un nuevo adopter.",
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente un adopter",
        description="Actualiza uno o mas campos de un adopter existente.",
    ),
    update=extend_schema(
        summary="Actualizar un adopter",
        description="Actualiza todos los campos editables de un adopter existente.",
    ),
    destroy=extend_schema(
        summary="Eliminar un adopter",
        description="Elimina definitivamente un adopter.",
    ),
)
class AdopterViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,
):
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdopterFilter

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.service = AdopterService()

    def get_queryset(self):
        return self.service.list_adopters()

    def get_serializer_class(self):
        return AdopterReadSerializer if self.action in ("list", "retrieve") else AdopterWriteSerializer

    def perform_create(self, serializer):
        serializer.instance = self.service.create_adopter(serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = self.service.update_adopter(serializer.instance.id, serializer.validated_data)

    def perform_destroy(self, instance):
        self.service.delete_adopter(instance.id)
