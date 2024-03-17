from django.utils import timezone
from django.db import models

from authx.models import CustomUser


class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.start_time = timezone.now()
        super().save(*args, **kwargs)

    def end_session(self):
        self.end_time = timezone.now()
        self.save()
