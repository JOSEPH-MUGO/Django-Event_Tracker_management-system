from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import PasswordResetView

from django.contrib.auth import  login, logout as auth_logout,get_user_model
from .forms import *
from EventRecord.models import Event
from django.contrib import messages
from .auth_backends import EmailAuthBackend
from employee.forms import EmployeeForm
from django.db import transaction
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
import logging




from django.core.mail import send_mail




def register(request):
    if not request.user.is_staff:
        return redirect('login')  # Only admin can register employees

    if request.method == 'POST':
        
       
        employee_form = EmployeeForm(request.POST)
        if employee_form.is_valid():
            try:
                with transaction.atomic():
                    employee = employee_form.save()
                    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                    employee.admin.set_password(password)
                    employee.admin.save()
                    
                    print(f"User: {employee}, Password: {password}")
                   # Send email with credentials
                    send_mail(
                        'Your account credentials',
                        f'Your account has been created. Email: {employee.admin.email}, Password: {password}',
                        'josephithanwa@gmail.com',
                        [employee.admin.email],
                        fail_silently=False,
                    )

                    messages.success(request, 'Employee registered successfully.')
                    return redirect('adminViewEmployee')
            except Exception as e:
                messages.error(request, f'An error occurred while creating the employee: {e}')
        else:
             
             print(employee_form.errors)
             messages.error(request, 'Invalid form data.')
    else:
       
        
        employee_form = EmployeeForm()

    return render(request, 'admin/adminV/employee.html', {'form2': employee_form})    


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
            
   
    return render(request, 'registration/login.html', context)
#logout view 
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


#password reset
logger = logging.getLogger(__name__)
class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        logger.debug("Form is Valid")
        UserModel = get_user_model()
        email=form.cleaned_data['email']
        user =UserModel.objects.filter(email=email, is_active = True).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            current_site = get_current_site(self.request)
            reset_url = reverse('password_reset_confirm',kwargs={'uidb64':uid, 'token': token})
            reset_url = f'http://{current_site.domain}{reset_url}'

            send_mail(
                'Password Reset',
                f' We received your request to reset password, Please follow this link to reset your password:{reset_url}',
                'josephithanwa@gmail.com',
                [user.email],
                fail_silently= False,
            )
            return super().form_valid(form)
        else:
            logger.debug("No active user found for email: %s", email)
            form.add_error('email', 'There is no active user associated with this email address. Please provide the correct email address')
            form.is_valid = False
            return self.form_invalid(form)
        






#employee dashboard
def dashboard(request):
    user = request.user
    if user is not None:

        event_count = Event.objects.count()
        context = { 'event_count': event_count}
        return render(request, 'account/dashboard.html',context)
    
  
        
