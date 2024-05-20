from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm

from django.contrib import messages



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit =False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            messages.success(request,'You have successfully registered!')
            return render(request, 'registration/login.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})
    


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
            username=cd['username'],
            password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Login successfully')
                else:
                    return HttpResponse('Disabled account')

            else:
                return HttpResponse('wrong username or password!')
    else:
        form =LoginForm()
        return render(request, 'account/login.html', {'form': form})

def logout(request):
    messages.warning( request, 'You have logout!')
    return redirect('login') 
        
@login_required(login_url='login')
def dashboard(request):
    context = { 'section': 'dashboard'}
    return render(request, 'account/dashboard.html',context)
  
        
