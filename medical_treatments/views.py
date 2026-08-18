from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema_view, extend_schema
from rest_framework import mixins, viewsets

from medical_treatments.filters import MedicalTreatmentFilter
from medical_treatments.serializers import MedicalTreatmentReadSerializer, MedicalTreatmentWriteSerializer
from medical_treatments.services import MedicalTreatmentService

@extend_schema(tags=["MedicalTreatments"])
@extend_schema_view(
    list=extend_schema(
        summary="Listar medical_treatments",
        description="Devuelve la lista paginada de medical_treatments.",
        parameters=[
            OpenApiParameter(name="animal", description="Filtra por id de animal exacto."),
            OpenApiParameter(name="veterinarian", description="Filtra por id de veterinario exacto."),
            OpenApiParameter(name="status", description="Filtra por estado exacto."),
        ],
    ),
    retrieve=extend_schema(
        summary="Obtener un medical_treatment",
        description="Devuelve el detalle de un medical_treatment por su id (ULID).",
    ),
    create=extend_schema(
        summary="Registrar un medical_treatment",
        description="Da de alta un nuevo medical_treatment.",
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente un medical_treatment",
        description="Actualiza uno o mas campos de un medical_treatment existente.",
    ),
    update=extend_schema(
        summary="Actualizar un medical_treatment",
        description="Actualiza todos los campos editables de un medical_treatment existente.",
    ),
    destroy=extend_schema(
        summary="Eliminar un medical_treatment",
        description="Elimina definitivamente un medical_treatment.",
    ),
)
class MedicalTreatmentViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,
):
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend]
    filterset_class = MedicalTreatmentFilter

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.service = MedicalTreatmentService()

    def get_queryset(self):
        return self.service.list_medical_treatments()

    def get_serializer_class(self):
        return MedicalTreatmentReadSerializer if self.action in ("list", "retrieve") else MedicalTreatmentWriteSerializer

    def perform_create(self, serializer):
        serializer.instance = self.service.create_medical_treatment(serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = self.service.update_medical_treatment(serializer.instance.id, serializer.validated_data)

    def perform_destroy(self, instance):
        self.service.delete_medical_treatment(instance.id)
