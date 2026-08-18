from django.contrib import admin
from vaccination_records.models import VaccinationRecord

@admin.register(VaccinationRecord)
class VaccinationRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "animal", "status", "applied_at", "created_at")
    list_filter = ("animal", "status")
    search_fields = ("id", "name", "animal")
    readonly_fields = ("id", "created_at", "updated_at")
