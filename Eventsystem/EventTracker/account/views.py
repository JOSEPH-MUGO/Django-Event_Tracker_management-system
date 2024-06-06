from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import views as auth_views
from django.contrib.auth import login, logout as auth_logout, get_user_model
from .forms import *
from EventRecord.models import Event
from django.contrib import messages
from .auth_backends import EmailAuthBackend
from employee.forms import EmployeeForm
from employee.models import Employee
from django.db import transaction
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from django.contrib.sites.shortcuts import get_current_site
import logging
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.views import PasswordResetView
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
def CustomPasswordResetView(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():

            data = form.cleaned_data['email']
            email = User.objects.filter(Q(email=data))
            if email.exists():
                for user in email:
                    subject = 'Password Request'
                    email_template_name = 'registration/password_messge.txt'
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

                    except:
                        return HttpResponse('invalid Header')
                    return redirect(reverse('password_reset'))
    else:
        form = PasswordResetForm()

    context = {
        'form': form

    }
    return render(request, 'registration/password_reset_form.html', context)


logger = logging.getLogger(__name__)

"""
class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('password_reset')
  

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = get_user_model().objects.filter(pk=self.kwargs.get('uidb64')).first()
        if user:
            employee = user.employee
            kwargs['phone'] = employee.phone  
        return kwargs
    
    def form_valid(self, form):
        logger.debug("Form is Valid")
        UserModel = get_user_model()
        email = form.cleaned_data['email']
        user = UserModel.objects.filter(email=email, is_active=True).first()
        if user:
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            current_site = get_current_site(self.request)
            reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
            reset_url = f'http://{current_site.domain}{reset_url}'

            send_mail(
                'Password Reset',
                f' We received your request to reset your password. Please follow this link to reset your password: {reset_url}',
                'josephithanwa@gmail.com',
                [user.email],
                fail_silently=False,
            )
            messages.success(self.request, 'We have sent instructions to your email for resetting your password. If you do not receive an email, please confirm if you entered the correct email address you registered with.')
        else:
            messages.error(self.request, 'There is no active user associated with this email address.')
            logger.debug("No active user found for email: %s", email)
            return self.form_invalid(form)
        return super().form_valid(form)
"""


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('login')
    form_class = CustomSetPasswordForm

    def get_user(self, uidb64):
        # uidb64 = self.kwargs.get('uidb64')
        if uidb64 is None:
            return None
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None
        return user

    def form_valid(self, form):
        token = self.kwargs.get('token')
        uidb64 = self.kwargs.get('uidb64')
        user = self.get_user(uidb64)

        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            messages.success(
                self.request, 'Your password has been reset successfully.')
            return super().form_valid(form)
        else:
            messages.error(
                self.request, 'The reset token is invalid or expired. Please request a new password reset.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'


# employee dashboard
def dashboard(request):
    user = request.user
    if user is not None:

        event_count = Event.objects.count()
        context = {'event_count': event_count}
        return render(request, 'account/dashboard.html', context)


"""
    def dispatch(self, request, *args, **kwargs):
        logger.debug(f"Dispatch called with kwargs: {kwargs}")
        self.user = self.get_user(*args, **kwargs)
        if not self.user:
            logger.error("User not found during dispatch.")
        return super().dispatch(request, *args, **kwargs)
 
    """
