from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.fields import TextInput
from django.forms.models import ModelForm

from django_yandex_intensive import settings

from .models import Profile


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


class EditUserForm(ModelForm):
    class Meta:
        model = User

        fields = (
            User.first_name.field.name,
            User.last_name.field.name,
            User.email.field.name,
        )
