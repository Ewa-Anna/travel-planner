from django.contrib import admin

from .models import Trip, Participant


class TripAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_date",
        "end_date",
        "organizer",
    )


class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "trip",
        "participant",
    )


admin.site.register(Trip, TripAdmin)
admin.site.register(Participant, ParticipantAdmin)
