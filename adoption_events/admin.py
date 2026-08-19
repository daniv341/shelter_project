from django.contrib import admin
from adoption_events.models import AdoptionEvent

@admin.register(AdoptionEvent)
class AdoptionEventAdmin(admin.ModelAdmin):
    list_display = ("id", "animal", "adopter", "adoption_application", "status", "created_at")
    list_filter = ("animal", "adopter", "adoption_application", "status")
    search_fields = ("id", "animal", "adopter", "adoption_application", "status")
    readonly_fields = ("id", "created_at", "updated_at")
