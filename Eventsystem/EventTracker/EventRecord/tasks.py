from celery import shared_task
from .models import Event

@shared_task
def update_event_statuses():
    events = Event.objects.all()
    for event in events:
        event.update_status()
