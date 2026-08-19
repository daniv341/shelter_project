from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema_view, extend_schema
from rest_framework import mixins, viewsets

from caretaker_assignments.filters import CaretakerAssignmentFilter
from caretaker_assignments.serializers import CaretakerAssignmentReadSerializer, CaretakerAssignmentWriteSerializer
from caretaker_assignments.services import CaretakerAssignmentService

@extend_schema(tags=["CaretakerAssignments"])
@extend_schema_view(
    list=extend_schema(
        summary="Listar caretaker_assignments",
        description="Devuelve la lista paginada de caretaker_assignments.",
        parameters=[
            OpenApiParameter(name="animal", description="Filtra por id de animal exacto."),
            OpenApiParameter(name="caretaker", description="Filtra por id de caretaker exacto."),
            OpenApiParameter(name="status", description="Filtra por estado exacto."),
        ],
    ),
    retrieve=extend_schema(
        summary="Obtener un caretaker_assignment",
        description="Devuelve el detalle de un caretaker_assignment por su id (ULID).",
    ),
    create=extend_schema(
        summary="Registrar un caretaker_assignment",
        description="Da de alta un nuevo caretaker_assignment.",
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente un caretaker_assignment",
        description="Actualiza uno o mas campos de un caretaker_assignment existente.",
    ),
    update=extend_schema(
        summary="Actualizar un caretaker_assignment",
        description="Actualiza todos los campos editables de un caretaker_assignment existente.",
    ),
    destroy=extend_schema(
        summary="Eliminar un caretaker_assignment",
        description="Elimina definitivamente un caretaker_assignment.",
    ),
)
class CaretakerAssignmentViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,
):
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend]
    filterset_class = CaretakerAssignmentFilter

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.service = CaretakerAssignmentService()

    def get_queryset(self):
        return self.service.list_caretaker_assignments()

    def get_serializer_class(self):
        return CaretakerAssignmentReadSerializer if self.action in ("list", "retrieve") else CaretakerAssignmentWriteSerializer

    def perform_create(self, serializer):
        serializer.instance = self.service.create_caretaker_assignment(serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = self.service.update_caretaker_assignment(serializer.instance.id, serializer.validated_data)

    def perform_destroy(self, instance):
        self.service.delete_caretaker_assignment(instance.id)
