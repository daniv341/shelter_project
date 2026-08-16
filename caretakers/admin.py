from django.contrib import admin
from caretakers.models import Caretaker


@admin.register(Caretaker)
class CaretakerAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("id", "full_name", "dni", "email")
    readonly_fields = ("id", "created_at", "updated_at")