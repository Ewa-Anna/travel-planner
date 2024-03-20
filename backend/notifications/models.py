from django.db import models


class Notification(models.Model):
    message = models.CharField(max_length=100)

    def __str__(self):
        return f"Message: {self.message}"
