from django import forms
from .models import *
from .utils import validatePassword

from django.core.exceptions import ValidationError
#from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import random
import string
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import PasswordResetForm

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

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, user_email, user_first_name, user_last_name, user_phone, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_email = user_email
        self.user_first_name = user_first_name
        self.user_last_name = user_last_name
        self.user_phone = user_phone

    def clean_new_password(self):
        cleaned_data = super().clean()
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        # Check if passwords match
        if new_password1 != new_password2:
            raise forms.ValidationError("The passwords do not match.")

        password = new_password1

        # Validate password
        try:
            validatePassword(password, self.user_email, self.user_first_name, self.user_last_name, self.user_phone)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)

        return cleaned_data

















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