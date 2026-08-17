from django.contrib import admin
from veterinarians.models import Veterinatian

@admin.register(Veterinatian)
class VeterinatianAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("id", "name")
    readonly_fields = ("id", "created_at", "updated_at")
