
from django.core.management.base import BaseCommand
from EventRecord.models import Event

class Command(BaseCommand):
    help = 'Update the status of events based on the end date'

    def handle(self, *args, **kwargs):
        events = Event.objects.all()
        for event in events:
            event.update_status()
        self.stdout.write(self.style.SUCCESS('Successfully updated event statuses'))