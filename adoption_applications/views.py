from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema_view, extend_schema
from rest_framework import mixins, viewsets

from adoption_applications.filters import AdoptionApplicationFilter
from adoption_applications.serializers import AdoptionApplicationReadSerializer, AdoptionApplicationWriteSerializer
from adoption_applications.services import AdoptionApplicationService

@extend_schema(tags=["AdoptionApplications"])
@extend_schema_view(
    list=extend_schema(
        summary="Listar adoption_applications",
        description="Devuelve la lista paginada de adoption_applications.",
        parameters=[
            OpenApiParameter(name="animal", description="Filtra por id de animal exacto."),
            OpenApiParameter(name="adopter", description="Filtra por id de adopter exacto."),
            OpenApiParameter(name="status", description="Filtra por estado exacto."),
        ],
    ),
    retrieve=extend_schema(
        summary="Obtener un adoption_application",
        description="Devuelve el detalle de un adoption_application por su id (ULID).",
    ),
    create=extend_schema(
        summary="Registrar un adoption_application",
        description="Da de alta un nuevo adoption_application.",
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente un adoption_application",
        description="Actualiza uno o mas campos de un adoption_application existente.",
    ),
    update=extend_schema(
        summary="Actualizar un adoption_application",
        description="Actualiza todos los campos editables de un adoption_application existente.",
    ),
    destroy=extend_schema(
        summary="Eliminar un adoption_application",
        description="Elimina definitivamente un adoption_application.",
    ),
)
class AdoptionApplicationViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,
):
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdoptionApplicationFilter

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.service = AdoptionApplicationService()

    def get_queryset(self):
        return self.service.list_adoption_applications()

    def get_serializer_class(self):
        return AdoptionApplicationReadSerializer if self.action in ("list", "retrieve") else AdoptionApplicationWriteSerializer

    def perform_create(self, serializer):
        serializer.instance = self.service.create_adoption_application(serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = self.service.update_adoption_application(serializer.instance.id, serializer.validated_data)

    def perform_destroy(self, instance):
        self.service.delete_adoption_application(instance.id)
