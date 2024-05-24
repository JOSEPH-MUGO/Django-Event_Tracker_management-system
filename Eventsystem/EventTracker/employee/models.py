from django.db import models
from account.models import CustomUser

# Create your models here.


class Employee(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=13, unique=True)  
    
    verified = models.BooleanField(default=False)
    
   

    def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name
