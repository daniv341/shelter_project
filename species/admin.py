from django.contrib import admin
from species.models import Species

@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("id", "name")
    readonly_fields = ("id", "created_at", "updated_at")
