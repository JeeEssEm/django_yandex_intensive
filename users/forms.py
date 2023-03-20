from django.contrib.auth.forms import UserCreationForm

from django_yandex_intensive import settings


class SignUpForm(UserCreationForm):
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.is_staff = False
        user.is_active = settings.DEBUG or settings.ACTIVATED_USER
        user.save()
