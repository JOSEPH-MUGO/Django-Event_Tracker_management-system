from django import forms
from .models import *
from account.forms import FormSettings
from tinymce.widgets import TinyMCE
from django.core.exceptions import ValidationError


class EventForm(FormSettings):
    event_type = forms.ModelChoiceField(queryset=EventCategory.objects.all(),widget=forms.Select(attrs={'class':'form-control','id':'category'}),required=True,label='Category', empty_label='Select a category')
    start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter title of the event'}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control','rows': 5,'placeholder': 'write a description of the event'}))
    venue = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter venue of the event'}))
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter location of the event'}))

    class Meta:
        model= Event
        fields = ['event_type','title','description','venue','location','start_date', 'end_date','status']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("End date should be later than start date.")
        
        return cleaned_data

class AssignForm(FormSettings):
    assign_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Select a date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'Select a time'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'type': 'textarea', 'rows': 3, 'placeholder': 'What do you expect from the employee about this event?'}))

    class Meta:
        model = Assignment
        fields = ['event', 'department', 'employee', 'assign_date', 'time', 'message']

    def __init__(self, department_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event'].queryset = Event.objects.filter(status='active').order_by('-id')
        self.fields['event'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select an event'})
        self.fields['department'].queryset = Department.objects.all()
        self.fields['department'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select a department', 'id': 'department-select'})
        self.fields['employee'].queryset = Employee.objects.none()
        self.fields['employee'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select an employee', 'id': 'employee-select'})

        if department_id:
            self.fields['employee'].queryset = Employee.objects.filter(department_id=department_id)
        
      

    def clean(self):
        cleaned_data = super().clean()
        event = cleaned_data.get('event')
        employee = cleaned_data.get('employee')

        if event and employee:
            # Check if the employee is already assigned to another event that starts on the same date
            if Assignment.objects.filter(
                employee=employee,
                event__start_date=event.start_date
            ).exclude(id=self.instance.id).exists():
                raise ValidationError('Employee is already assigned to another event starting on the same date.')

        return cleaned_data
class EventCategoryForm(FormSettings):
    class Meta:
        model = EventCategory
        fields = ['event_type']


class ReportForm(FormSettings):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = Report
        fields = ['content','image']

