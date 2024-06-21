from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout as auth_logout, get_user_model
from .forms import *
from EventRecord.models import Event
from django.contrib import messages
from .auth_backends import EmailAuthBackend
from employee.forms import EmployeeForm
from django.db import transaction
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q


def register(request):
    if not request.user.is_staff:
        return redirect('login')  # Only admin can register employees

    if request.method == 'POST':

        employee_form = EmployeeForm(request.POST)
        if employee_form.is_valid():
            try:
                with transaction.atomic():

                    employee = employee_form.save()
                    password = ''.join(random.choices(
                        string.ascii_letters + string.digits, k=8))
                    employee.admin.set_password(password)
                    employee.admin.save()

                    messages.success(
                        request, 'Employee registered successfully.')
                    return redirect('adminViewEmployee')
            except Exception as e:
                messages.error(
                    request, f'An error occurred while creating the employee: {e}')
        else:

            print(employee_form.errors)
            messages.error(request, 'Invalid form data.')
    else:

        employee_form = EmployeeForm()

    return render(request, 'admin/adminV/employee.html', {'form2': employee_form})


def custom_login(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("admin_dashboard"))
        else:
            return redirect(reverse("dashboard"))

    context = {}
    if request.method == 'POST':

        email_backend = EmailAuthBackend()
        user = email_backend.authenticate(request, username=request.POST.get(
            'email'), password=request.POST.get('password'))
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
# logout view


def custom_logout(request):
    user = request.user
    context = {}
    if user.is_authenticated:
        auth_logout(request)
        messages.warning(request, 'You have logout!')

    else:
        messages.error(request, "You need to login to perform this action")
    context['messages'] = messages.get_messages(request)
    return redirect(reverse("login"))


# password reset
def customPasswordResetView(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():

            data = form.cleaned_data['email']
            email = User.objects.filter(Q(email=data))
            if email.exists():
                for user in email:
                    subject = 'Password Request'
                    email_template_name = 'registration/message.txt'
                    paramaters = {
                        'email': user.email,
                        'domain': get_current_site(request).domain,
                        'site_name': 'Event Tracker',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, paramaters)
                    try:
                        send_mail(subject, email, '', [
                              user.email], fail_silently=False)
                        messages.success(request, 'We have sent instructions to your email for resetting your password. If you do not receive an email, please confirm if you entered the correct email address you registered with.')

                    except User.DoesNotExist:
                        messages.error(request, ' The entered email address is not registered!')
                        return HttpResponse('invalid Header')
                    return redirect(reverse('password_reset'))
    else:
        form = PasswordResetForm()

    context = {
        'form': form

    }
    return render(request, 'registration/password_reset_form.html', context)



def customPasswordResetConfirm(request,uidb64= None, token=None):
    UserModel = get_user_model()
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError,OverflowError,UserModel.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        if request.method =='POST':
            form = CustomSetPasswordForm(user,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Your new password has been set')
                return redirect(reverse('login'))
        else:
            form = CustomSetPasswordForm(user)
        
    else:
        messages.error(request,'The reset token is invalid or expired. Please request a new password reset')
        return redirect('password_reset')
    context = {
        'form':form
    }
    return render(request,'registration/password_reset_confirm.html',context)
        
        




