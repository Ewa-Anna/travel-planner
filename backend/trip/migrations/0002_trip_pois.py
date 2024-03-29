# Generated by Django 5.0.2 on 2024-03-12 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0001_initial"),
        ("trip", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="trip",
            name="pois",
            field=models.ManyToManyField(
                related_name="trips",
                to="locations.poi",
                verbose_name="Points of Interest",
            ),
        ),
    ]
