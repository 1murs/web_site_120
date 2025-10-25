from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "phone", "city", "created_at"]
    list_filter = ["city", "created_at"]
    search_fields = ["first_name", "last_name", "email"]
    fieldsets = (
        ("Основна інформація", {"fields": ("first_name", "last_name", "email")}),
        ("Контакти", {"fields": ("phone", "city", "address")}),
        ("Безпека", {"fields": ("password",)}),
    )
