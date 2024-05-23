from django import forms
from .models import *
from account.forms import FormSettings





class EventForm(FormSettings):
    event_type = forms.ModelChoiceField(queryset=EventCategory.objects.all(),widget=forms.Select(attrs={'class':'form-control'}),required=True)
    class Meta:
        model= Event
        fields = ['event_type','title','description','venue','location','start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of event'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the event...'}),
            'venue': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the venue of the event'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class AssignForm(FormSettings):
    class Meta:
        model = Assignment
        fields = ['event','employee']

class ReportForm(FormSettings):
    Notes = forms.CharField(widget=forms.Textarea(attrs={'rows':5}))
    class Meta:
        model = Report
        fields = ['Notes']


class EventCategoryForm(FormSettings):
    class Meta:
        model = EventCategory
        fields = ['event_type']

class ReportFileForm(FormSettings):
    class Meta:
        model= ReportFile
        fields = ['file']
