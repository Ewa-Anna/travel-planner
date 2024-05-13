from django.contrib import admin

from .models import Friendship


class FriendshipAdmin(admin.ModelAdmin):
    list_display = ["user", "friend"]


admin.site.register(Friendship, FriendshipAdmin)
