from celery import shared_task
from .models import Event
from django.utils import timezone

@shared_task
def update_event_status():
    events = Event.objects.filter(status='active', end_date__lte=timezone.now())
    for event in events:
        event.end_date = event.end_date.replace(hour=23, minute=59, second=59)  
        if event.end_date < timezone.now():
            event.status = 'completed'
            event.save()