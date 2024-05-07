from django.apps import AppConfig


class LittlelemonapiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "LittleLemonApi"

    def ready(self) -> None:
        import LittleLemonApi.signals 
