from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema_view, extend_schema
from rest_framework import mixins, viewsets

from caretakers.filters import CaretakerFilter
from caretakers.serializers import CaretakerReadSerializer, CaretakerWriteSerializer
from caretakers.services import CaretakerService


@extend_schema_view(
    list=extend_schema(
        summary="Listar caretakers",
        description="Devuelve la lista paginada de caretakers del refugio, ",
        parameters=[
            OpenApiParameter(name="status", description="Filtra por estado exacto."),
        ],
    ),
    retrieve=extend_schema(
        summary="Obtener un caretaker",
        description="Devuelve el detalle de un caretaker por su id (ULID).",
    ),
    create=extend_schema(
        summary="Registrar un caretaker",
        description="Da de alta un nuevo caretaker en el refugio.",
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente un caretaker",
        description="Actualiza uno o más campos de un caretaker existente.",
    ),
    update=extend_schema(
        summary="Actualizar un caretaker",
        description="Actualiza todos los campos editables de un caretaker existente.",
    ),
    destroy=extend_schema(
        summary="Eliminar un caretaker",
        description="Elimina definitivamente un caretaker del refugio.",
    ),
)
class CaretakerViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,
):
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend]
    filterset_class = CaretakerFilter

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.service = CaretakerService()

    def get_queryset(self):
        return self.service.list_caretakers()

    def get_serializer_class(self):
        return CaretakerReadSerializer if self.action in ("list", "retrieve") else CaretakerWriteSerializer

    def perform_create(self, serializer):
        serializer.instance = self.service.create_caretaker(serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = self.service.update_caretaker(serializer.instance.id, serializer.validated_data)

    def perform_destroy(self, instance):
        self.service.delete_caretaker(instance.id)