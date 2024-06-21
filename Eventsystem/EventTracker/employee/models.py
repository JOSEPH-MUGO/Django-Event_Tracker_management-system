from django.db import models
from account.models import User

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name}"
    def employee_count(self):
        return self.employee_set.count()

class Employee(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.admin.last_name}, {self.admin.first_name}"

    