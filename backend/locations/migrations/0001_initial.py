# Generated by Django 5.0.2 on 2024-03-12 16:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, unique=True, verbose_name="Name"),
                ),
                (
                    "iso_code",
                    models.CharField(blank=True, max_length=2, verbose_name="ISO Code"),
                ),
                (
                    "currency",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="Currency"
                    ),
                ),
                (
                    "primary_language",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="Primary Language"
                    ),
                ),
                (
                    "flag",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="country_flags/",
                        verbose_name="Flag",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, unique=True, verbose_name="Name"),
                ),
                (
                    "population",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Population"
                    ),
                ),
                (
                    "latitude",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        max_digits=9,
                        null=True,
                        verbose_name="Latitude",
                    ),
                ),
                (
                    "longitude",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        max_digits=9,
                        null=True,
                        verbose_name="Longitude",
                    ),
                ),
                (
                    "region",
                    models.CharField(blank=True, max_length=100, verbose_name="Region"),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cities",
                        to="locations.country",
                        verbose_name="Country",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="POI",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Name")),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Description"),
                ),
                (
                    "location_latitude",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        max_digits=9,
                        null=True,
                        verbose_name="Location Latitude",
                    ),
                ),
                (
                    "location_longitude",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        max_digits=9,
                        null=True,
                        verbose_name="Location Longitude",
                    ),
                ),
                (
                    "opening_hours",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="Opening Hours"
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pois",
                        to="locations.city",
                        verbose_name="City",
                    ),
                ),
            ],
        ),
    ]