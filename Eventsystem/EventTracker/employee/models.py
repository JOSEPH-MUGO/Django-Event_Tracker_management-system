from django.db import models
from account.models import User

# Create your models here.


class Employee(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13, unique=True)
     
    def __str__(self):
        return f"{self.admin.last_name}, {self.admin.first_name}"
