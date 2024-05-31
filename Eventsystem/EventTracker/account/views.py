from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import  PasswordResetConfirmView
from django.contrib.auth import views as auth_views
from django.contrib.auth import  login, logout as auth_logout,get_user_model
from .forms import *
from django.urls import reverse_lazy
from EventRecord.models import Event
from django.contrib import messages
from .auth_backends import EmailAuthBackend
from employee.forms import EmployeeForm
from employee.models import Employee
from django.db import transaction
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
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
                        f'Hello! {employee.admin.first_name}, Your account for Event tracker system has been created successfully using Email: {employee.admin.email},Use this Password: {password} to login to the system. You can change it later if you want. Thanks',
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
class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('password_reset')
    email_template_name = 'registration/password_reset_email.html'
    #form_class = CustomSetPasswordForm


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = get_user_model().objects.filter(pk=self.kwargs.get('uidb64')).first()
        if user:
            kwargs['phone'] = user.employee.phone  # Assuming employee is related to the user
        return kwargs
    
    def form_valid(self, form):
        logger.debug("Form is Valid")
        UserModel = get_user_model()
        email=form.cleaned_data['email']
        user =UserModel.objects.filter(email=email, is_active = True).first()
        if user:
            from django.utils.http import urlsafe_base64_encode
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            current_site = get_current_site(self.request)
            reset_url = reverse('password_reset_confirm',kwargs={'uidb64':uid, 'token': token})
            reset_url = f'http://{current_site.domain}{reset_url}'

            send_mail(
                'Password Reset',
                f' We received your request to reset your password, Please follow this link to reset your password:{reset_url}',
                'josephithanwa@gmail.com',
                [user.email],
                fail_silently= False,
            )
            messages.success(self.request, 'We have sent instructions to your email for resetting your password. If you do not receive an email, please confirm if you entered the correct email address you registered with.')
            
        else:
            messages.error(self.request, 'There is no active user associated with this email address.')
            logger.debug("No active user found for email: %s", email)
            
            return self.form_invalid(form)
        return super().form_valid(form)
        




class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name= 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('login')
    form_class = CustomSetPasswordForm
    
    def dispatch(self, request, *args, **kwargs):
        # Set the user attribute before calling the parent dispatch method
        self.user = self.get_user()
        return super().dispatch(request, *args, **kwargs)
    
    def get_user(self):
      
        uidb64 = self.kwargs['uidb64']
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.get_user()
        return kwargs



    def form_valid(self, form):
        logger.debug("Form is Valid")
        token =self.kwargs.get('token')
        user = get_user_model().objects.filter(pk=self.kwargs.get('uidb64')).first()
        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            return super().form_valid(form)
        else:
            messages.error(self.request, 'The reset token is invalid or expired. please request a new password reset.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        logger.debug("Form is Invalid")
        return super().form_invalid(form)


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name= 'registration/password_reset_complete.html'


#employee dashboard
def dashboard(request):
    user = request.user
    if user is not None:

        event_count = Event.objects.count()
        context = { 'event_count': event_count}
        return render(request, 'account/dashboard.html',context)
    
  
        
