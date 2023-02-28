import core.models

import django.core.validators
import django.db.models
from django.utils.safestring import mark_safe

from sorl.thumbnail import get_thumbnail

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

    def get_main_image(self):
        if self.main_image is not None:
            return self.main_image.image_thumb()
        return 'Нет изображения'

    get_main_image.short_description = 'превью'
    get_main_image.allow_tags = True

    class Meta:
        verbose_name_plural = 'товары'
        verbose_name = 'товар'

    def __str__(self):
        return self.text[:15]


class Image(django.db.models.Model):
    image = django.db.models.ImageField(
        'Прикрепите изображение',
        upload_to='catalog/',
    )
    item = django.db.models.OneToOneField(
        to=Item,
        on_delete=django.db.models.deletion.CASCADE,
        related_name='main_image',
        verbose_name='товар'
    )

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    def get_image_x1280(self):
        return get_thumbnail(self.image, '1280', quality=51)

    def get_image_300x300(self):
        return get_thumbnail(self.image, '300x300', crop='center', quality=51)

    def image_thumb(self):
        if self.image:
            return mark_safe(
                f'<img src="{self.get_image_300x300().url}" width=50>'
            )
        return 'Нет изображения'

    image_thumb.short_description = 'превью'
    image_thumb.allow_tags = True

    def __str__(self):
        return self.image.url


class Gallery(django.db.models.Model):
    image = django.db.models.ImageField(
        'Прикрепите изображение',
        upload_to='catalog/',
        null=True,
    )
    item = django.db.models.ForeignKey(
        to=Item,
        on_delete=django.db.models.deletion.CASCADE,
        verbose_name='товар'
    )

    class Meta:
        verbose_name_plural = 'галереи'
        verbose_name = 'галерея'

    def get_image_300x300(self):
        return get_thumbnail(self.image, '300x300', crop='center', quality=51)

    def image_thumb(self):
        if self.image:
            return mark_safe(
                f'<img src="{self.get_image_300x300().url}" width=50>'
            )
        return 'Нет изображения'

    def __str__(self):
        return self.image.url
