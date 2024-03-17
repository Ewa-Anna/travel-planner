from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver

from .models import UserActivity


@receiver(user_logged_out)
def end_user_session(sender, user, request, **kwargs):
    try:
        user_activity = UserActivity.objects.get(user=user, end_time__isnull=True)
        user_activity.end_session()
    except UserActivity.DoesNotExist:
        pass
