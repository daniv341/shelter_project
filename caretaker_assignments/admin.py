from django.contrib import admin
from caretaker_assignments.models import CaretakerAssignment

@admin.register(CaretakerAssignment)
class CaretakerAssignmentAdmin(admin.ModelAdmin):
    list_display = ("id", "animal", "caretaker", "status", "created_at")
    list_filter = ("animal", "caretaker", "status")
    search_fields = ("id", "animal", "caretaker", "status")
    readonly_fields = ("id", "created_at", "updated_at")
