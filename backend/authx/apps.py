from django.apps import AppConfig


class AuthxConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authx"

    def ready(self):
        # pylint: disable=import-outside-toplevel, unused-import
        import authx.signals  # noqa: F401
