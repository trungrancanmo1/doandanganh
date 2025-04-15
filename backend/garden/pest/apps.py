from django.apps import AppConfig


class PestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pest'

    def ready(self):
        from . import signals