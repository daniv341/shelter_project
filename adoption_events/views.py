from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema_view, extend_schema
from rest_framework import mixins, viewsets

from adoption_events.filters import AdoptionEventFilter
from adoption_events.serializers import AdoptionEventReadSerializer, AdoptionEventWriteSerializer
from adoption_events.services import AdoptionEventService

@extend_schema(tags=["AdoptionEvents"])
@extend_schema_view(
    list=extend_schema(
        summary="Listar adoption_events",
        description="Devuelve la lista paginada de adoption_events.",
        parameters=[
            OpenApiParameter(name="animal", description="Filtra por id de animal exacto."),
            OpenApiParameter(name="adopter", description="Filtra por id de adopter exacto."),
            OpenApiParameter(name="adoption_application", description="Filtra por id de adoption_application exacto."),
            OpenApiParameter(name="status", description="Filtra por estado exacto."),
        ],
    ),
    retrieve=extend_schema(
        summary="Obtener un adoption_event",
        description="Devuelve el detalle de un adoption_event por su id (ULID).",
    ),
    create=extend_schema(
        summary="Registrar un adoption_event",
        description="Da de alta un nuevo adoption_event.",
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente un adoption_event",
        description="Actualiza uno o mas campos de un adoption_event existente.",
    ),
    update=extend_schema(
        summary="Actualizar un adoption_event",
        description="Actualiza todos los campos editables de un adoption_event existente.",
    ),
    destroy=extend_schema(
        summary="Eliminar un adoption_event",
        description="Elimina definitivamente un adoption_event.",
    ),
)
class AdoptionEventViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,
):
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdoptionEventFilter

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.service = AdoptionEventService()

    def get_queryset(self):
        return self.service.list_adoption_events()

    def get_serializer_class(self):
        return AdoptionEventReadSerializer if self.action in ("list", "retrieve") else AdoptionEventWriteSerializer

    def perform_create(self, serializer):
        serializer.instance = self.service.create_adoption_event(serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = self.service.update_adoption_event(serializer.instance.id, serializer.validated_data)

    def perform_destroy(self, instance):
        self.service.delete_adoption_event(instance.id)
