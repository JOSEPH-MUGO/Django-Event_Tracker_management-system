from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

class EmailAuthBackend(ModelBackend):
    def authenticate(self,request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
            logger.debug(f"Found user: {user}")
        except UserModel.DoesNotExist:
            logger.debug(f"User with email {username} does not exist")
            return None
        else:
            if user.check_password(password):
                logger.debug("Password check passed")
                return user
            else:
                logger.debug("Password check failed")
        return None
