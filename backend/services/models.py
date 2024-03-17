from django.db import models


class Accommodation(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    details = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    amenities = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    def total_price(self):
        number_of_nights = (self.checkout_date - self.checkin_date).days
        total_price = self.price_per_night * number_of_nights
        return total_price


class Transportation(models.Model):
    TRANSPORTATION_TYPES = (
        ("car", "Car"),
        ("bus", "Bus"),
        ("train", "Train"),
        ("plane", "Plane"),
        ("other", "Other"),
    )
    name = models.CharField(max_length=100)
    departure_location = models.CharField(max_length=100)
    arrival_location = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TRANSPORTATION_TYPES)

    def __str__(self):
        return f"{self.name}"
