from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema_view, extend_schema
from rest_framework import mixins, viewsets

from vaccination_records.filters import VaccinationRecordFilter
from vaccination_records.serializers import VaccinationRecordReadSerializer, VaccinationRecordWriteSerializer
from vaccination_records.services import VaccinationRecordService

@extend_schema(tags=["VaccinationRecords"])
@extend_schema_view(
    list=extend_schema(
        summary="Listar vaccination_records",
        description="Devuelve la lista paginada de vaccination_records.",
        parameters=[
            OpenApiParameter(name="animal", description="Filtra por id de animal exacto."),
            OpenApiParameter(name="status", description="Filtra por estado exacto."),
        ],
    ),
    retrieve=extend_schema(
        summary="Obtener un vaccination_record",
        description="Devuelve el detalle de un vaccination_record por su id (ULID).",
    ),
    create=extend_schema(
        summary="Registrar un vaccination_record",
        description="Da de alta un nuevo vaccination_record.",
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente un vaccination_record",
        description="Actualiza uno o mas campos de un vaccination_record existente.",
    ),
    update=extend_schema(
        summary="Actualizar un vaccination_record",
        description="Actualiza todos los campos editables de un vaccination_record existente.",
    ),
    destroy=extend_schema(
        summary="Eliminar un vaccination_record",
        description="Elimina definitivamente un vaccination_record.",
    ),
)
class VaccinationRecordViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,
):
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend]
    filterset_class = VaccinationRecordFilter

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.service = VaccinationRecordService()

    def get_queryset(self):
        return self.service.list_vaccination_records()

    def get_serializer_class(self):
        return VaccinationRecordReadSerializer if self.action in ("list", "retrieve") else VaccinationRecordWriteSerializer

    def perform_create(self, serializer):
        serializer.instance = self.service.create_vaccination_record(serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = self.service.update_vaccination_record(serializer.instance.id, serializer.validated_data)

    def perform_destroy(self, instance):
        self.service.delete_vaccination_record(instance.id)
