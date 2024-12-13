from django.apps import AppConfig

"""Configuration of the overall django app
   This will ensure that the primary key that will support larger integers
   It sets the name of the app
"""
class DndcharactercustomizerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'new_app'

    """This overrides the ready method
       When the app is ready this ensures the signal handler defined are registered
    """
    def ready(self):
        import new_app.signals