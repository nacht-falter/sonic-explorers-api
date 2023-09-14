from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "profiles"

    # Instructions for importing signals:
    # https://www.geeksforgeeks.org/how-to-create-and-use-signals-in-django/
    def ready(self):
        import profiles.signals
