from django import forms
from .models import *
from account.forms import FormSettings





class EventForm(FormSettings):
    event_type = forms.ModelChoiceField(queryset=EventCategory.objects.all(),widget=forms.Select(attrs={'class':'form-control'}),required=True,label='Category')
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'})) 

    class Meta:
        model= Event
        fields = ['event_type','title','description','venue','location','start_date', 'end_date']
         
       
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
