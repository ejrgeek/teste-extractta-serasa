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
        "is_staff",
        "is_active",
    ]

    search_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
    ]

    list_filter = [
        "is_staff",
        "is_active",
    ]
