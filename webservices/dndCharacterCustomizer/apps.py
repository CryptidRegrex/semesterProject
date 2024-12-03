from django.apps import AppConfig


class DndcharactercustomizerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dndCharacterCustomizer'

    def ready(self):
        import dndCharacterCustomizer.signals