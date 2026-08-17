from django.contrib import admin
from caretakers.models import Caretaker

# registrar el modelo Caretaker en el admin
@admin.register(Caretaker)
class CaretakerAdmin(admin.ModelAdmin):
    # list_display para mostrar los campos en la lista de objetos del admin
    list_display = ("id", "full_name", "email", "status", "created_at")
    # list_filter para filtrar por status
    list_filter = ("status",)
    # search_fields para buscar por los campos especificados
    search_fields = ("id", "full_name", "dni", "email")
    # readonly_fields para hacer los campos de solo lectura
    readonly_fields = ("id", "created_at", "updated_at")