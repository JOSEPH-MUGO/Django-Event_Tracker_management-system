from django import forms
from .models import Event


EventCategory = [('training', 'Training'), ('workshop', 'Workshop'), ('seminar', 'Seminar')]


class EventForm(forms.ModelForm):
    event_type = forms.ChoiceField(choices=EventCategory,widget=forms.Select(attrs={'class':'form-control'}),required=True)
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

