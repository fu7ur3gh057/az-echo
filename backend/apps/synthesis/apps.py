from django.apps import AppConfig


class SynthesisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.synthesis'

    def ready(self):
        import apps.synthesis.signals
