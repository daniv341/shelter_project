from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema_view, extend_schema
from rest_framework import mixins, viewsets

from species.filters import SpeciesFilter
from species.serializers import SpeciesReadSerializer, SpeciesWriteSerializer
from species.services import SpeciesService

@extend_schema(tags=["Species"])
@extend_schema_view(
    list=extend_schema(
        summary="Listar species",
        description="Devuelve la lista paginada de species.",
        parameters=[
            OpenApiParameter(name="status", description="Filtra por estado exacto."),
        ],
    ),
    retrieve=extend_schema(
        summary="Obtener un species",
        description="Devuelve el detalle de un species por su id (ULID).",
    ),
    create=extend_schema(
        summary="Registrar un species",
        description="Da de alta un nuevo species.",
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente un species",
        description="Actualiza uno o mas campos de un species existente.",
    ),
    update=extend_schema(
        summary="Actualizar un species",
        description="Actualiza todos los campos editables de un species existente.",
    ),
    destroy=extend_schema(
        summary="Eliminar un species",
        description="Elimina definitivamente un species.",
    ),
)
class SpeciesViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,
):
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend]
    filterset_class = SpeciesFilter

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.service = SpeciesService()

    def get_queryset(self):
        return self.service.list_species()

    def get_serializer_class(self):
        return SpeciesReadSerializer if self.action in ("list", "retrieve") else SpeciesWriteSerializer

    def perform_create(self, serializer):
        serializer.instance = self.service.create_species(serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = self.service.update_species(serializer.instance.id, serializer.validated_data)

    def perform_destroy(self, instance):
        self.service.delete_species(instance.id)
