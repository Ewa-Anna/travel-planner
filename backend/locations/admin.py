from django.contrib import admin

from .models import City, Country, POI


class CityAdmin(admin.ModelAdmin):
    list_display = ["name", "country"]
    list_filter = ["country"]
    search_fields = ["name"]


class CountryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


class POIAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "city"]
    list_filter = ["city__country", "city"]
    search_fields = ["name"]


admin.site.register(City, CityAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(POI, POIAdmin)
