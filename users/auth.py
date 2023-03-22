from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailLoginAuth(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}

        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
            else:
                return None

        except User.DoesNotExist:
            return None
