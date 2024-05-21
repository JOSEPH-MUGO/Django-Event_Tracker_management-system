from django.db import models

# Create your models here.
class Event(models.Model):
    event_type = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    venue = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_date = models.DateField(auto_created=True)
    end_date = models.DateField(auto_created=True)

    def __str__(self):
        return self.title
    

    
