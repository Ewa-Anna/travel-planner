from django.contrib import admin

from .models import UserActivity


class UserActivityAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]


admin.site.register(UserActivity, UserActivityAdmin)
