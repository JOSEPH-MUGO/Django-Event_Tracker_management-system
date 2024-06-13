from django import forms
from .models import *
from account.forms import FormSettings
from django.core.exceptions import  ValidationError
import re


class EmployeeForm(FormSettings):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'tel','placeholder':'Enter employee phone number'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(),widget=forms.Select(attrs={'class':'form-control'}),required=True,label='Department', empty_label='Select a employee department')
    department_id = forms.CharField(widget=forms.HiddenInput(), required=False,label='')


    class Meta:
        model = Employee
        fields = ['phone','department']
    def validatePhone(phone):
        pattern = r'^(\+254)?[0-9]{9}$'
        if not re.match(pattern, phone):
            raise ValidationError('Please enter a valid phone number')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        department_id = kwargs.pop('department_id', None)
        if department_id:
            self.fields['department'].queryset = Department.objects.filter(pk=department_id)
            self.initial['department'] = department_id  # Pre-populate the department field

       
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