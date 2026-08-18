from django.contrib import admin
from medical_treatments.models import MedicalTreatment

@admin.register(MedicalTreatment)
class MedicalTreatmentAdmin(admin.ModelAdmin):
    list_display = ("id", "diagnostic", "animal", "veterinarian", "status", "started_at")
    list_filter = ("animal", "veterinarian", "status")
    search_fields = ("id", "diagnostic", "animal", "veterinarian")
    readonly_fields = ("id", "created_at", "updated_at")
