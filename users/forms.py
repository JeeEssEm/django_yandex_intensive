from django.contrib.auth.forms import (
    AuthenticationForm, UserChangeForm, UserCreationForm
)
from django.core.exceptions import ValidationError
from django.forms.fields import TextInput
from django.forms.models import ModelForm

from django_yandex_intensive import settings

from .models import Profile, User


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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        users_count = User.objects.filter(email=email).exists()
        if users_count != 0:
            raise ValidationError('Такой email уже существует')
        return email


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
        model = User

        fields = (
            User.first_name.field.name,
            User.last_name.field.name,
            User.email.field.name,
        )
        exclude = (
            User.password.field.name,
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email == self.instance.email:
            return email

        users_count = User.objects.filter(email=email).exists()
        if users_count:
            raise ValidationError('Такой email уже существует')
        return email


class LoginForm(AuthenticationForm):
    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя/email'
