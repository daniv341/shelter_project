"""
views.py

Las vistas deben ser muy delgadas: solo reciben la petición HTTP,
validan el serializer y delegan al servicio correspondiente. No
contienen lógica de negocio.
"""
from __future__ import annotations

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import mixins, viewsets

from animals.filters import AnimalFilter
from animals.serializers import AnimalReadSerializer, AnimalWriteSerializer
from animals.services import AnimalService

@extend_schema(tags=["Animals"])
@extend_schema_view(
    list=extend_schema(
        summary="Listar animales",
        description="Devuelve la lista paginada de animales del refugio, "
        "con soporte de filtros por especie, nombre, sexo, estado de "
        "adopción y estado médico.",
        parameters=[
            OpenApiParameter(name="species", description="Filtra por especie (contiene, case-insensitive)."),
            OpenApiParameter(name="sex", description="Filtra por sexo exacto."),
            OpenApiParameter(name="adoption_status", description="Filtra por estado de adopción exacto."),
            OpenApiParameter(name="medical_status", description="Filtra por estado médico exacto."),
        ],
    ),
    retrieve=extend_schema(
        summary="Obtener un animal",
        description="Devuelve el detalle de un animal por su id (ULID).",
    ),
    create=extend_schema(
        summary="Registrar un animal",
        description="Da de alta un nuevo animal en el refugio.",
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente un animal",
        description="Actualiza uno o más campos de un animal existente.",
    ),
    update=extend_schema(
        summary="Actualizar un animal",
        description="Actualiza todos los campos editables de un animal existente.",
    ),
    destroy=extend_schema(
        summary="Eliminar un animal",
        description="Elimina definitivamente un animal del refugio.",
    ),
)
class AnimalViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """CRUD de animales del refugio.

    La resolución de queryset usa el selector; las mutaciones se
    delegan al AnimalService, que a su vez usa el repository. Esto
    mantiene la vista libre de lógica de negocio.
    """

    lookup_field = "id"
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnimalFilter

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.service = AnimalService()

    def get_queryset(self):
        return self.service.list_animals()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AnimalReadSerializer
        return AnimalWriteSerializer

    def perform_create(self, serializer: AnimalWriteSerializer) -> None:
        animal = self.service.create_animal(serializer.validated_data)
        serializer.instance = animal

    def perform_update(self, serializer: AnimalWriteSerializer) -> None:
        animal = self.service.update_animal(serializer.instance.id, serializer.validated_data)
        serializer.instance = animal

    def perform_destroy(self, instance) -> None:
        self.service.delete_animal(instance.id)
