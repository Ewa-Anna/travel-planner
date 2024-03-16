from datetime import date

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from taggit.managers import TaggableManager

from authx.models import CustomUser
from trip.models import Trip


def get_trip_upload_path(instance, filename):
    current_date = date.today()
    trip_name = instance.journal_entry.trip.name
    return f"photos/{current_date}/{trip_name}/{filename}"


class TravelJournal(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, verbose_name="Title")
    notes = models.TextField()
    tags = TaggableManager()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Journal Entry for {self.trip.name} by {self.user.username} on {self.created}"


class Photos(models.Model):
    photo = models.FileField(upload_to=get_trip_upload_path)
    journal_entry = models.ForeignKey(
        "TravelJournal", on_delete=models.CASCADE, related_name="photos"
    )
    tags = TaggableManager()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.journal_entry}"


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    recommended = models.BooleanField(default=False)
    pros = models.TextField(blank=True)
    cons = models.TextField(blank=True)
    visibility = models.CharField(
        max_length=10,
        choices=[
            ("public", "Public"),
            ("private", "Private"),
            ("friends", "Shared with Friends"),
        ],
        default="public",
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - Rating: {self.rating}"
