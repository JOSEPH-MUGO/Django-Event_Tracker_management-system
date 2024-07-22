
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)
class AccountCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user  # Who is the current user?
        
        logger.debug(f"User: {user}, Module: {modulename}, Path: {request.path}")

        # Exempt paths for authentication
        exempt_paths = [
            reverse('token_obtain_pair'),
            reverse('token_refresh'),
            reverse('login'),
            reverse('password_reset'),
            reverse('password_reset_confirm', kwargs={'uidb64': view_kwargs.get('uidb64'), 'token': view_kwargs.get('token')}),
            reverse('password_reset_complete'),
        ]

        if any(request.path == path for path in exempt_paths) or modulename == 'django.contrib.auth.views':
            return None

        if user.is_authenticated:
            if user.user_type == '1':  # Admin
                logger.debug(f"Access granted to admin user: {user.email}")
                return None
            elif user.user_type == '2':  # Employee
                logger.debug(f"Access granted to employee user: {user.email}")
                return None
            else:
                logger.debug(f"Unauthorized user type: {user.user_type}")
                return redirect(reverse('login'))
        else:
            logger.debug("User not authenticated, redirecting to login.")
            return redirect(reverse('login'))