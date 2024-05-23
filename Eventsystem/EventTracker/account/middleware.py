from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages


class AccountCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user  # Who is the current user ?
        if user.is_authenticated:
            if user.user_type == '1':  # Admin
                if modulename == 'EventRecord.views':
                    error = True
                    if request.path == reverse('event_list'):
                        pass
                    else:
                        messages.error(
                            request, "You do not have access to this resource")
                        return redirect(reverse('admin_dashboard'))
            elif user.user_type == '2':  # Employee
                if modulename == 'administrator.views':
                    messages.error(
                        request, "You do not have access to this resource")
                    return redirect(reverse('dashboard'))
            else:  # None of the aforementioned ? Please take the user to login page
                return redirect(reverse('login'))
        else:
         # If the path is login or has anything to do with authentication, pass
            if request.path == reverse('login') or request.path == reverse('register') or modulename == 'django.contrib.auth.views' or request.path == reverse('login'):
                pass
            elif modulename == 'administrator.views' or modulename == 'employee.views':
                # If visitor tries to access administrator or employee functions
                messages.error(
                    request, "You need to be logged in to perform this operation")
                return redirect(reverse('login'))
            else:
                return redirect(reverse('login'))