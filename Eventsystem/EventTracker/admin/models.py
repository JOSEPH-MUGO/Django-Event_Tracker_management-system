from django.db import models

# Create your models here.
class Event(models.Model):
    Event_Type = models.CharField(max_length=50)
    Title = models.CharField(max_length=100)
    Description = models.TextField()
    Venue = models.CharField(max_length=100)
    Location = models.CharField(max_length=100)
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField(auto_created=True)

    def __str__(self):
        return self.Title
    

    
