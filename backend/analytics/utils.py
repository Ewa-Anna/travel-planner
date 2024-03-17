from .models import UserActivity


def calculate_total_time_spent(user):
    sessions = UserActivity.objects.filter(user=user, end_time__isnull=False)
    total_time = sum(
        (session.end_time - session.start_time).total_seconds() for session in sessions
    )
    total_hours = total_time / 3600
    return total_hours
