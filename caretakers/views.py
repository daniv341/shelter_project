from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema_view, extend_schema
from rest_framework import mixins, viewsets

from caretakers.filters import CaretakerFilter
from caretakers.serializers import CaretakerReadSerializer, CaretakerWriteSerializer
from caretakers.services import CaretakerService

@extend_schema(tags=["Caretakers"])
@extend_schema_view(
    # agregar un esquema para list
    list=extend_schema(
        summary="Listar caretakers",
        description="Devuelve la lista paginada de caretakers del refugio, ",
        # agregar un parámetro de query para filtrar por status 
        parameters=[
            OpenApiParameter(name="status", description="Filtra por estado exacto."),
        ],
    ),
    # agregar un esquema para retrieve, create, update, partial_update y destroy
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
    # los mixins permiten definir las acciones del viewset de manera modular, y GenericViewSet permite definir un viewset genérico que puede ser extendido por los mixins
    mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,
):
    # lookup_field permite definir el campo que se usará para buscar un objeto en retrieve, update y destroy; por defecto es "pk", pero en este caso se usa "id" 
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend]
    filterset_class = CaretakerFilter

    # __init__ permite inicializar el viewset con un servicio de caretakers, que se usará para delegar la lógica de negocio y separar las responsabilidades
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.service = CaretakerService()

    # define el queryset que se usará para  obtener la lista de caretakers
    def get_queryset(self):
        return self.service.list_caretakers()

    # define el serializer que se usará para cada acción del viewset; si la acción es list o retrieve, se usa el serializer de lectura, si es create, update o destroy, se usa el serializer de escritura
    def get_serializer_class(self):
        return CaretakerReadSerializer if self.action in ("list", "retrieve") else CaretakerWriteSerializer

    # perform create es para delegar la creación de un caretaker al servicio, usando los datos validados del serializer
    def perform_create(self, serializer):
        serializer.instance = self.service.create_caretaker(serializer.validated_data)

    # perform update es para delegar la actualización de un caretaker al servicio, usando los datos validados del serializer
    def perform_update(self, serializer):
        serializer.instance = self.service.update_caretaker(serializer.instance.id, serializer.validated_data)

    # perform destroy es para delegar la eliminación de un caretaker al servicio
    def perform_destroy(self, instance):
        self.service.delete_caretaker(instance.id)