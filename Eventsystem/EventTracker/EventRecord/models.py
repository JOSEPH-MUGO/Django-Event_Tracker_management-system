from django.db import models
from account.models import User
from employee.models import Employee
from django.utils import timezone 

# Create your models here.
class EventCategory(models.Model):
    event_type = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.event_type
    
class Event(models.Model):
    event_type = models.ForeignKey(EventCategory,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    venue = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_date = models.DateField(auto_created=True)
    end_date = models.DateField()

    def __str__(self):
        return self.title
    
class Assignment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    assign_date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)

    def __str__(self):
        return f'{self.employee.admin.email} assigned to {self.event.title}'

class Report(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    Notes  = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    proof = models.FileField(upload_to='reports/')

class ReportFile(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    file = models.FileField(upload_to='report/')


    
