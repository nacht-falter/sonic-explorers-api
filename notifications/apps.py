from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notifications"

    # Instructions for importing signals:
    # https://www.geeksforgeeks.org/how-to-create-and-use-signals-in-django/
    def ready(self):
        import notifications.signals
