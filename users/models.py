import pathlib

from annoying.fields import AutoOneToOneField

from django.contrib.auth.models import User
from django.db import models

from .managers import UserManager


class Profile(models.Model):
    def get_upload_folder(instance, filename):
        return (
                pathlib.Path('users')
                / f'ava_{str(instance.user.id)}.{filename.split(".")[-1]}'
        )

    user = AutoOneToOneField(to=User, on_delete=models.deletion.CASCADE)
    birthday = models.DateField('дата рождения', null=True, blank=True)
    image = models.ImageField('аватарка', null=True, blank=True,
                              upload_to=get_upload_folder)
    coffee_count = models.IntegerField('кофе', default=0)

    class Meta:
        verbose_name = 'дополнительная информация'

    def __str__(self):
        return 'Профиль'


class ProxyUser(User):
    objects = UserManager()

    class Meta:
        proxy = True
