from django.core.management.base import BaseCommand
from django.utils import timezone
from EventRecord.models import Event

class Command(BaseCommand):
    help = 'Update the status of events based on the end date'

    def handle(self, *args, **kwargs):
        events = Event.objects.all()
        now = timezone.now()
        for event in events:
            if event.status != 'disabled':
                if event.end_date <= now:
                    event.status = 'completed'
                else:
                    event.status = 'active'
                event.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated event statuses'))
