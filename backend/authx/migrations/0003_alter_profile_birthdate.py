# Generated by Django 5.0.2 on 2024-03-06 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authx", "0002_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="birthdate",
            field=models.DateField(blank=True, null=True, verbose_name="Date of Birth"),
        ),
    ]
