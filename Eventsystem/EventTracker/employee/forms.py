from django import forms
from .models import *
from account.forms import FormSettings


class EmployeeForm(FormSettings):
    class Meta:
        model = Employee
        fields = ['phone']

