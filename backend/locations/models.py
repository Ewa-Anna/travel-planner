from django.db import models


class Country(models.Model):
    name = models.CharField(
        max_length=100, unique=True, blank=False, verbose_name="Name"
    )
    iso_code = models.CharField(max_length=2, blank=True, verbose_name="ISO Code")
    currency = models.CharField(max_length=50, blank=True, verbose_name="Currency")
    primary_language = models.CharField(
        max_length=50, blank=True, verbose_name="Primary Language"
    )
    flag = models.ImageField(
        upload_to="country_flags/", blank=True, null=True, verbose_name="Flag"
    )

    def __str__(self):
        return f"Country: {self.name}"


class City(models.Model):
    name = models.CharField(
        max_length=100, unique=True, blank=False, verbose_name="Name"
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="cities", verbose_name="Country"
    )
    population = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Population"
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Latitude"
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Longitude"
    )
    region = models.CharField(max_length=100, blank=True, verbose_name="Region")

    def __str__(self):
        return f"City: {self.name} in {self.country.name}"


class POI(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name="Name")
    description = models.TextField(blank=True, verbose_name="Description")
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="pois", verbose_name="City"
    )
    location_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name="Location Latitude",
    )
    location_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name="Location Longitude",
    )
    opening_hours = models.CharField(
        max_length=200, blank=True, verbose_name="Opening Hours"
    )

    def __str__(self):
        return f"{self.name} ({self.city.name})"
