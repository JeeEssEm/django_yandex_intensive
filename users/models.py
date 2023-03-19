from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.deletion.CASCADE)
    birthday = models.DateField('дата рождения', null=True, blank=True)
    image = models.ImageField('аватарка', null=True, blank=True)
    coffee_count = models.IntegerField('кофе', default=0)

    class Meta:
        verbose_name = 'Дополнительная информация'
