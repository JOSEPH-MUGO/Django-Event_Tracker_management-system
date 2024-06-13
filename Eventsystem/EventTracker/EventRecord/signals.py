from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from .models import Assignment
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@receiver(pre_save, sender=Assignment)
def save_old_employee(sender, instance, **kwargs):
    if instance.pk:
        instance._old_employee = Assignment.objects.get(pk=instance.pk).employee
    else:
        instance._old_employee = None

@receiver(post_save, sender=Assignment)
def event_mail(sender, instance, created, **kwargs):
    employee = instance.employee
    event = instance.event
    subject = f'You have been assigned to an event: {event.title}'
    
    # Email content template
    email_content = render_to_string('emails/assignment_email.html', {'employee': employee, 'event': event, 'message':instance.message})
    plain_message = strip_tags(email_content)

    if created:
        # Send email to new employee if assignment is created
        send_mail(subject, plain_message, '', [employee.admin.email], fail_silently=False)
    else:
        # Check if employee has changed
        old_employee = instance._old_employee
        if old_employee and old_employee != employee:
            # Notify old employee of reassignment
            old_subject = f'You have been reassigned from an event: {event.title}'
            old_email_content = render_to_string('emails/assignment_reassigned.html', {'employee': old_employee, 'event': event, 'message':instance.message})
            old_plain_message = strip_tags(old_email_content)
            send_mail(old_subject, old_plain_message, '', [old_employee.admin.email], fail_silently=False)
        
        # Notify new employee of updated assignment
        send_mail(subject, plain_message, '', [employee.admin.email], fail_silently=False)
