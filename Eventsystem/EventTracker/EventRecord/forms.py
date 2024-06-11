from django import forms
from .models import *
from account.forms import FormSettings





class EventForm(FormSettings):
    event_type = forms.ModelChoiceField(queryset=EventCategory.objects.all(),widget=forms.Select(attrs={'class':'form-control'}),required=True,label='Category', empty_label='Select a category')
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'})) 
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter event title'}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Enter event description'}))
    venue = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter event venue'}))
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter event location'}))

    class Meta:
        model= Event
        fields = ['event_type','title','description','venue','location','start_date', 'end_date']
        
      
       
class AssignForm(FormSettings):
    assign_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'form-control','placeholder': 'Select a date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time','class':'form-control','placeholder': 'Select a time'}))

    class Meta:
        model = Assignment
        fields = ['event','employee','assign_date','time']
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['event'].queryset = Event.objects.all()
            self.fields['employee'].queryset = Employee.objects.all()
            self.fields['event'].widget.attrs.update({'class': 'form-control'})
            self.fields['event'].widget.attrs['placeholder'] = "Select an event"  # Update placeholder attribute
            self.fields['employee'].widget.attrs.update({'class': 'form-control'})
            self.fields['employee'].widget.attrs['placeholder'] = "Select an employee"
            

class ReportForm(FormSettings):
    Notes = forms.CharField(widget=forms.Textarea(attrs={'rows':5}))
    class Meta:
        model = Report
        fields = ['Notes','proof']

        def clean_pdf_report(self):
            pdf= self.cleaned_data.get('pdf_report')
            if pdf:
                if not pdf.name.endswith('.pdf'):
                    raise forms.ValidationError('The uploaded file must be a pdf document.')
                if pdf.size > 5*1024*1024:
                    raise forms.ValidationError('The PDF file size should not exceed 5 MB.')
            return pdf


class EventCategoryForm(FormSettings):
    class Meta:
        model = EventCategory
        fields = ['event_type']

class ReportFileForm(FormSettings):
    class Meta:
        model= ReportFile
        fields = ['file']
