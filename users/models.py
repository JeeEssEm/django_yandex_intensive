import pathlib

from annoying.fields import AutoOneToOneField

from core import utils

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver

from .managers import UserManager


User._meta.get_field('email')._unique = True  # NOQA


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


@receiver(models.signals.pre_save, sender=User)
def normalize_email(sender, instance, **kwargs):
    normalized_email = utils.normalize_email(instance.email)
    if normalized_email != instance.email:
        exists = User.objects.filter(email=normalized_email
                                     ).exclude(pk=instance.pk).exists()
        if exists:
            raise ValidationError('Такая почта уже существует')
        instance.email = normalized_email
        instance.save()
