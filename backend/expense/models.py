from django.db import models

from trip.models import Trip


class Expense(models.Model):
    EXPENSE_TYPES = [
        ("accommodation", "Accommodation"),
        ("transportation", "Transportation"),
        ("food", "Food"),
        ("poi", "POI"),
        ("activity", "Activity"),
        ("other", "Other"),
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=EXPENSE_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    details = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        ordering = ["-id"]
