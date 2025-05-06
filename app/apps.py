from django.core.management import call_command
from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        # This will run the management command when the app is ready
        call_command('create_periodic_task')
