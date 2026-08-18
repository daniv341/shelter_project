from django.contrib import admin
from veterinarians.models import Veterinarian

@admin.register(Veterinarian)
class VeterinarianAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("id", "full_name", "dni")
    readonly_fields = ("id", "created_at", "updated_at")
