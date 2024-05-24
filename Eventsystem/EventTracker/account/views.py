from django.shortcuts import render, redirect, reverse
#from django.http import HttpResponse
from django.contrib.auth import  login, logout as auth_logout
#from .forms import LoginForm
#from django.contrib.auth.decorators import login_required
from .forms import *
from EventRecord.models import Event
from django.contrib import messages
from .auth_backends import EmailAuthBackend
from employee.forms import EmployeeForm
from django.db import IntegrityError,transaction
from employee.models import Employee

 
def register(request):
    userForm = CustomUserForm(request.POST or None)
    employeeForm = EmployeeForm(request.POST or None)
    context = {
        'form1': userForm,
        'form2': employeeForm
    }

    if request.method == 'POST':
        if userForm.is_valid() and employeeForm.is_valid():
            try:
                with transaction.atomic():
                    user = userForm.save(commit=False)
                    user.save()
                    
                    employee = employeeForm.save(commit=False)
                    employee.admin = user
                    employee.email = user.email  # Assuming email should be the same as the user's email
                    employee.save()

                messages.success(request, "Your account was created successfully. You can now login.")
                return redirect(reverse('login'))
            except IntegrityError:
                messages.error(request, "An error occurred while creating the account. Please try again.")
        else:
            messages.error(request, "Provided credentials failed validation.")
    context['messages'] = messages.get_messages(request)
    
    return render(request, 'account/register.html', context)
    


def custom_login(request):
    if request.user.is_authenticated:
        if request.user.user_type =='1':
            return redirect(reverse("admin_dashboard"))
        else:
            return redirect(reverse("dashboard"))
    
    context = {}
    if request.method == 'POST':

        email_backend = EmailAuthBackend()
        user = email_backend.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        username = request.POST.get('email')
        password = request.POST.get('password')
        print('password', password)
        print("Email", username)
        
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if user.user_type == '1':
                return redirect(reverse("admin_dashboard"))
            else:
                return redirect(reverse("dashboard"))
        else:
            messages.error(request, "Invalid credentials provided, Try again!") 
            return redirect("/")
    context['messages'] = messages.get_messages(request)
    return render(request, 'registration/login.html', context)

def custom_logout(request):
    user = request.user
    context = {}
    if user.is_authenticated:
        auth_logout(request)
        messages.warning( request, 'You have logout!')
        
    else:
        messages.error(request, "You need to login to perform this action")
    context['messages'] = messages.get_messages(request)
    return redirect(reverse("login")) 
    
        

def dashboard(request):
    user = request.user
    if user is not None:

        event_count = Event.objects.count()
        context = { 'event_count': event_count}
        return render(request, 'account/dashboard.html',context)
    
  
        
