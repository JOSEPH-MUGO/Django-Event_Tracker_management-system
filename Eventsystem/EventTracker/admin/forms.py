from django import forms
from .models import Event



EventCategory = [('training','Training'),('workshop','Workshop'),('seminar','Seminar')]

class EventForm(forms.ModelForm):
    Event_Type = forms.CharField(widget=forms.Select(choices=EventCategory, attrs={'class':'form-control'}),required=True)
    Title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Type of event'}),required=True)
    Description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Describe the event...'}))
    Venue = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the venue of the event'}),required=True)
    Location= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Location'}),required=True)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))
    

    class Meta:
        model= Event
        fields = {'Title','Description','Venue','Location','start_date', 'end_date'}

