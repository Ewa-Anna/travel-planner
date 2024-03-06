from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Profile


class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_admin",
    )
    list_filter = ("is_active", "is_staff", "is_admin")
    search_fields = ("username", "email", "first_name", "last_name")


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "birthdate",
    )


admin.site.unregister(Group)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
