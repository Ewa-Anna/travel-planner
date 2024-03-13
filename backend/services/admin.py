from django.contrib import admin

from .models import Accommodation, Transportation


class AccomodationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "checkin_date", "checkout_date")


class TransportationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type")


admin.site.register(Accommodation, AccomodationAdmin)
admin.site.register(Transportation, TransportationAdmin)
