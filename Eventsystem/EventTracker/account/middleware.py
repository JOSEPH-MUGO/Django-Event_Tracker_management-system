import logging
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages

# Initialize the logger
logger = logging.getLogger(__name__)

class AccountCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user  # Current user
        
        logger.debug(f"User: {user}, Path: {request.path}, Module: {modulename}")
        
        if user.is_authenticated:
            logger.debug(f"Authenticated user type: {user.user_type}")
            if user.user_type == '1':  # Admin
                if modulename == 'EventRecord.views':
                    allowed_paths = [
                        reverse('viewEvents'),
                        reverse('updateEvent'),
                        reverse('deleteEvent'),
                        reverse('createEventCategory'),
                        reverse('password_reset'),
                    ]
                    # Handle specific view_kwargs for updating and deleting events
                    if 'uidb64' in view_kwargs and 'token' in view_kwargs:
                        allowed_paths.append(reverse('password_reset_confirm', kwargs=view_kwargs))
                    
                    # Check if request path is in allowed paths
                    for allowed_path in allowed_paths:
                        if request.path == allowed_path:
                            return None
                    
                    messages.error(request, "You do not have access to this resource")
                    logger.warning(f"Admin access denied for path: {request.path}")
                    return redirect(reverse('admin_dashboard'))

            elif user.user_type == '2':  # Employee
                if modulename == 'administrator.views':
                    messages.error(request, "You do not have access to this resource")
                    logger.warning(f"Employee access denied for path: {request.path}")
                    return redirect(reverse('dashboard'))
            else:  # Undefined user_type, redirect to login
                logger.warning(f"Undefined user type for user: {user}")
                return redirect(reverse('login'))
        
        else:  # User is not authenticated
            allowed_paths = [
                reverse('login'),
                reverse('password_reset'),
                reverse('password_reset_complete'),
            ]
            if 'uidb64' in view_kwargs and 'token' in view_kwargs:
                allowed_paths.append(reverse('password_reset_confirm', kwargs=view_kwargs))

            if request.path in allowed_paths or modulename == 'django.contrib.auth.views':
                return None
            else:
                if modulename in ['administrator.views', 'employee.views']:
                    messages.error(request, "You need to be logged in to perform this operation")
                logger.warning(f"Unauthenticated access attempt to path: {request.path}")
                return redirect(reverse('login'))

        return None  # Ensure the view is processed if no redirects are needed
