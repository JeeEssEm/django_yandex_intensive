import core.models

import django.core.validators
import django.db.models

from . import validators


class Category(core.models.AbstractItem, core.models.AbstractName):
    weight = django.db.models.PositiveIntegerField(
        'Масса',
        help_text='Введите массу, значение не больше 32767 и не меньше 1',
        default=100,
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(32767),
        ],
    )

    class Meta:
        verbose_name_plural = 'категории'
        verbose_name = 'категория'


class Tag(core.models.AbstractItem, core.models.AbstractName):
    class Meta:
        verbose_name_plural = 'теги'
        verbose_name = 'тег'


class Item(core.models.AbstractItem):
    text = django.db.models.TextField(
        'Описание',
        validators=[
            validators.ValidateMustContain('превосходно', 'роскошно'),
        ],
    )

    category = django.db.models.ForeignKey(
        to=Category,
        on_delete=django.db.models.deletion.CASCADE,
        verbose_name='категория',
    )

    tags = django.db.models.ManyToManyField(Tag)

    class Meta:
        verbose_name_plural = 'товары'
        verbose_name = 'товар'

    def __str__(self):
        return self.text[:15]
