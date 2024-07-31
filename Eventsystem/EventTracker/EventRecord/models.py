from django.db import models
from account.models import User
from employee.models import Employee, Department
from django.utils import timezone
from tinymce import models as tinymce_models
from django.core.exceptions import ValidationError

class EventCategory(models.Model):
    event_type = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_type

class Event(models.Model):
    StatusChoices = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('disabled', 'Disabled'),
    ]

    event_type = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    venue = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=StatusChoices)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.update_status()
        super().save(*args, **kwargs)

    def update_status(self):
        if self.status != 'disabled':
            if self.end_date <= timezone.now():
                self.status = 'completed'
            else:
                self.status = 'active'
            return True
        return False

    def disable_event(self):
        self.status = 'disabled'
        self.save()

class Assignment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    assign_date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    message = models.TextField(max_length=225)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.employee} assigned to {self.event.title}'

    def has_report(self):
        return self.report_set.exists()

    def clean(self):
        super().clean()
        if Assignment.objects.filter(employee=self.employee, event__start_date=self.event.start_date).exclude(id=self.id).exists():
            raise ValidationError('Employee is already assigned to another event starting on the same date.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Report(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.PROTECT)
    content = tinymce_models.HTMLField()
    image = models.ImageField(upload_to='report_images/')
    submitted_by = models.ForeignKey(Employee, on_delete=models.PROTECT)
    submitted_at = models.DateTimeField(default=timezone.now)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('disapproved', 'Disapproved'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message