from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):

    username = forms.CharField()
    Employee_ID = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','first_name','email')
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