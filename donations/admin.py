from django.contrib import admin
from donations.models import Donation

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("id", "adopter", "mount", "type_donation", "status", "created_at")
    list_filter = ("adopter", "type_donation", "status")
    search_fields = ("id", "adopter", "type_donation", "status")
    readonly_fields = ("id", "created_at", "updated_at")
