# Generated by Django 5.0.2 on 2024-03-16 16:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("trip", "0005_alter_trip_accommodations_alter_trip_transportations"),
    ]

    operations = [
        migrations.CreateModel(
            name="Expense",
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
                    "category",
                    models.CharField(
                        choices=[
                            ("accommodation", "Accommodation"),
                            ("transportation", "Transportation"),
                            ("food", "Food"),
                            ("poi", "POI"),
                            ("activity", "Activity"),
                            ("other", "Other"),
                        ],
                        max_length=20,
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("currency", models.CharField(max_length=3)),
                ("details", models.TextField(blank=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "trip",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="trip.trip"
                    ),
                ),
            ],
            options={
                "verbose_name": "Expense",
                "verbose_name_plural": "Expenses",
                "ordering": ["-id"],
            },
        ),
    ]