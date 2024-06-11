from django import forms
from .models import *
from account.forms import FormSettings
from django.core.exceptions import  ValidationError
import re


class EmployeeForm(FormSettings):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'tel','placeholder':'Enter employee phone number'}))


    class Meta:
        model = Employee
        fields = ['phone']
        def validatePhone(phone):
            pattern = r'^(\+254)?[0-9]{9}$'
            if not re.match(pattern, phone):
                raise ValidationError('Please enter a valid phone number')

       
class DepartmentForm(FormSettings):
     name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text','placeholder':'Enter name of the department'}))
     created_at =forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':'form-control','placeholder':'Select the date and time', 'type':'datetime-local','readonly': 'readonly',}),required=False)
     
     class Meta:
         model = Department
         fields = ['name']
         

     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  
            self.fields['created_at'].initial = self.instance.created_at.strftime('%Y-%m-%dT%H:%M')
        else:
            self.fields.pop('created_at')