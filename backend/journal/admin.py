from django.contrib import admin

from .models import TravelJournal, Photos, Review


class TravelJournalAdmin(admin.ModelAdmin):
    list_display = ["trip", "user", "title"]
    list_filter = ["trip", "user"]
    search_fields = ["trip__name", "user__username", "title"]
    readonly_fields = ["created", "updated"]


class PhotosAdmin(admin.ModelAdmin):
    list_display = ["journal_entry", "created"]
    list_filter = ["journal_entry", "created"]
    search_fields = ["journal_entry__trip__name"]
    readonly_fields = ["created"]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "trip", "rating", "date"]
    list_filter = ["user", "trip", "rating", "date"]
    search_fields = ["user__username", "trip__name", "rating"]
    readonly_fields = ["date"]


admin.site.register(TravelJournal, TravelJournalAdmin)
admin.site.register(Photos, PhotosAdmin)
admin.site.register(Review, ReviewAdmin)
