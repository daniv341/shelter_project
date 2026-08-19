from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema_view, extend_schema
from rest_framework import mixins, viewsets

from donations.filters import DonationFilter
from donations.serializers import DonationReadSerializer, DonationWriteSerializer
from donations.services import DonationService

@extend_schema(tags=["Donations"])
@extend_schema_view(
    list=extend_schema(
        summary="Listar donations",
        description="Devuelve la lista paginada de donations.",
        parameters=[
            OpenApiParameter(name="adopter", description="Filtra por id de adopter exacto."),
            OpenApiParameter(name="type_donation", description="Filtra por estado exacto."),
            OpenApiParameter(name="status", description="Filtra por estado exacto."),
        ],
    ),
    retrieve=extend_schema(
        summary="Obtener un donation",
        description="Devuelve el detalle de un donation por su id (ULID).",
    ),
    create=extend_schema(
        summary="Registrar un donation",
        description="Da de alta un nuevo donation.",
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente un donation",
        description="Actualiza uno o mas campos de un donation existente.",
    ),
    update=extend_schema(
        summary="Actualizar un donation",
        description="Actualiza todos los campos editables de un donation existente.",
    ),
    destroy=extend_schema(
        summary="Eliminar un donation",
        description="Elimina definitivamente un donation.",
    ),
)
class DonationViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,
):
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend]
    filterset_class = DonationFilter

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.service = DonationService()

    def get_queryset(self):
        return self.service.list_donations()

    def get_serializer_class(self):
        return DonationReadSerializer if self.action in ("list", "retrieve") else DonationWriteSerializer

    def perform_create(self, serializer):
        serializer.instance = self.service.create_donation(serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = self.service.update_donation(serializer.instance.id, serializer.validated_data)

    def perform_destroy(self, instance):
        self.service.delete_donation(instance.id)
