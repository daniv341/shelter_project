from django.contrib import admin
from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "user_name", "email", "status", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("id", "user_name", "email")
    readonly_fields = ("id", "created_at", "updated_at")