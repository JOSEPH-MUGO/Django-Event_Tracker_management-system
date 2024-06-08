from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from .models import Assignment
from django.template.loader import render_to_string

@receiver(post_save,sender=Assignment)
def event_mail(sender,instance,created,**kwargs):
    if created:
        employee = instance.employee
        event = instance.event

        subject =f'You have been assigned to an event: {event.title}'
        mail_template = 'EventRecord/event_details.txt'
        details = {f'The event is under the category of: {event.event_type.id}\n',
                   f'Title of the event: {event.title}\n'
                   f'Description of the event: {event.description}\n'
                   f'Venue where the event will be held: {event.venue}\n'
                   f'Location of the event: {event.location}\n'
                   f'Event will commerce on date: {event.start_date}\n'
                   f'Event will end on date: {event.end_date}\n'                   
                   }
        email = render_to_string(mail_template, details)
        send_mail(
            subject, email, '' ,[employee.admin.email],fail_silently=False
        )