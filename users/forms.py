from core import utils

from django.contrib.auth.forms import (
    AuthenticationForm, UserChangeForm, UserCreationForm
)
from django.core.exceptions import ValidationError
from django.forms.fields import TextInput
from django.forms.models import ModelForm


from django_yandex_intensive import settings

from .models import Profile, ProxyUser, User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            User.email.field.name,
            User.username.field.name,
        )

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.is_staff = False
        user.is_active = settings.DEBUG or settings.ACTIVATED_USER
        try:
            user.save()
            return user
        except ValidationError as exc:
            self.errors.update(exc)

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['email'] = utils.normalize_email(
            self.cleaned_data['email']
        )
        return cleaned_data


class EditProfileForm(ModelForm):
    class Meta:
        model = Profile

        fields = (
            Profile.birthday.field.name,
            Profile.image.field.name,
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[Profile.birthday.field.name].widget = TextInput(
            {
                'type': 'date'
            },
        )
        self.fields[Profile.birthday.field.name].initial = (
            kwargs.get('initial').get('birthday')
        )


class EditUserForm(UserChangeForm):
    password = None

    class Meta:
        model = ProxyUser

        fields = (
            ProxyUser.first_name.field.name,
            ProxyUser.last_name.field.name,
            ProxyUser.email.field.name,
        )

    def save(self, commit=True):
        try:
            return super(EditUserForm, self).save()
        except ValidationError as exc:
            self.errors.update('email', exc)

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['email'] = utils.normalize_email(
            self.cleaned_data['email']
        )
        return cleaned_data


class LoginForm(AuthenticationForm):
    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя/email'
