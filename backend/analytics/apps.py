from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "analytics"

    def ready(self):
        # pylint: disable=import-outside-toplevel, unused-import
        import analytics.signals  # noqa: F401
