from django.contrib import admin

from animals.models import Animal


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "species",
        "sex",
        "adoption_status",
        "medical_status",
        "created_at",
    )
    list_filter = ("species", "sex", "adoption_status", "medical_status")
    search_fields = ("id", "name", "species")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
