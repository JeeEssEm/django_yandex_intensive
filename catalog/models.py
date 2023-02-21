import core.models

import django.core.validators
import django.db.models

from . import validators


class Category(core.models.AbstractItem, core.models.AbstractName):
    weight = django.db.models.PositiveIntegerField(
        'Масса',
        default=100,
        validators=[
            django.core.validators.MinValueValidator(0),
            django.core.validators.MaxValueValidator(32767),
        ],
    )

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


class Tag(core.models.AbstractItem, core.models.AbstractName):
    class Meta:
        verbose_name_plural = 'Теги'
        verbose_name = 'Тег'


class Item(core.models.AbstractItem):
    text = django.db.models.TextField(
        'Описание',
        validators=[
            validators.contains_perfect_words,
        ],
    )

    category = django.db.models.ForeignKey(
        to=Category,
        on_delete=django.db.models.deletion.CASCADE,
        verbose_name='Категория',
        default=None,
    )

    tags = django.db.models.ManyToManyField(Tag)

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'

    def __str__(self):
        return self.text[:15]
