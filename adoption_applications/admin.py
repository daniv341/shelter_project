from django.contrib import admin
from adoption_applications.models import AdoptionApplication

@admin.register(AdoptionApplication)
class AdoptionApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "animal", "adopter", "status", "created_at")
    list_filter = ("animal", "adopter", "status")
    search_fields = ("id", "animal", "adopter", "status")
    readonly_fields = ("id", "created_at", "updated_at")
