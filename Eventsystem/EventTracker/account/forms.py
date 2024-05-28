from django import forms
from .models import *
#from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import random
import string

class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class UserForm(FormSettings):
    email = forms.EmailField(required=True)
    
   
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email']

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        user.password = make_password(password)
        if commit:
            user.save()
        return user,password


















"""
class LoginForm(forms.ModelForm):

    username = forms.CharField(widget=forms.TimeInput(attrs={'class':'form-control'}))
    Employee_ID = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','first_name','email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password']!= cd['password2']:
            raise forms.ValidationError('Password don\'t match.')
        return cd['password2'] 
  #allowing users edit their profile eg. firstname,lastname,email        
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        """