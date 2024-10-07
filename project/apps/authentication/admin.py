from django.contrib import admin
from apps.authentication.models.user import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
        "enrollment",
        "is_staff",
        "is_active",
    ]

    search_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "enrollment",
    ]

    list_filter = [
        "is_staff",
        "is_active",
    ]
