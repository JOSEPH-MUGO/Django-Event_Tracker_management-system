from django.apps import AppConfig


class EventRecordConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EventRecord'

    def ready(self):
        import EventRecord.signals
