from django import forms
from .models import *
from account.forms import FormSettings


class EmployeeForm(FormSettings):

    class Meta:
        model = Employee
        fields = ['phone']

    def save(self, commit=True):
        employee = super().save(commit=False)
        if commit:
            employee.admin.email = self.cleaned_data['email']
            employee.admin.save()
            employee.save()
        return employee

