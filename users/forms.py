from django.contrib.auth.forms import (
    AuthenticationForm, UserChangeForm, UserCreationForm
)
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
        user.save()
        return user


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
    class Meta:
        model = ProxyUser

        fields = (
            ProxyUser.first_name.field.name,
            ProxyUser.last_name.field.name,
            ProxyUser.email.field.name,
        )
        exclude = (
            ProxyUser.password.field.name,
        )


class LoginForm(AuthenticationForm):
    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя/email'
