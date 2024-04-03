from django.db import models
from django.core.exceptions import ValidationError

from authx.models import CustomUser
from locations.models import POI
from services.models import Accommodation, Transportation


class Trip(models.Model):
    name = models.CharField(
        max_length=100, unique=False, blank=False, verbose_name="Name"
    )
    start_date = models.DateField(blank=False, null=False, verbose_name="Start Date")
    end_date = models.DateField(blank=False, null=False, verbose_name="End Date")
    organizer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="Organizer",
        related_name="organized_trips",
    )
    pois = models.ManyToManyField(
        POI, related_name="trips", verbose_name="Points of Interest"
    )
    accommodations = models.ManyToManyField(
        Accommodation, related_name="trips", verbose_name="Accommodations"
    )
    transportations = models.ManyToManyField(
        Transportation, related_name="trips", verbose_name="Transportations"
    )

    class Meta:
        unique_together = [["name", "organizer"]]

    def __str__(self):
        return f"Trip: {self.name} organized by {self.organizer}"

    def clean(self):
        """
        Validate that the end date is greater than the start date.
        """
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be greater than the start date.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Participant(models.Model):
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, verbose_name="Trip", related_name="participants"
    )
    participant = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Participant",
        related_name="trips_participated",
    )

    class Meta:
        unique_together = ("trip", "participant")
        verbose_name = "Participant"

    def __str__(self):
        return f"{self.participant.username} in {self.trip.name}"
