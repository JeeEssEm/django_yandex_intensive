import core.models
import core.utils

import django.core.validators
import django.db.models
from django.utils.safestring import mark_safe

from sorl.thumbnail import get_thumbnail

from tinymce.models import HTMLField

from . import managers
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
    objects = managers.ItemManager()

    created_at = django.db.models.DateTimeField(auto_now_add=True)
    updated_at = django.db.models.DateTimeField(auto_now=True)

    text = HTMLField(
        'описание',
        validators=[
            validators.ValidateMustContain('превосходно', 'роскошно'),
        ],
    )
    is_on_main = django.db.models.BooleanField(
        'на главной странице',
        default=False
    )

    category = django.db.models.ForeignKey(
        to=Category,
        on_delete=django.db.models.deletion.CASCADE,
        verbose_name='категория',
    )

    tags = django.db.models.ManyToManyField(Tag)

    def get_image_thumb(self):
        if hasattr(self, 'main_image'):
            crop_img = get_thumbnail(
                self.main_image.image,
                '300x300',
                crop='center',
                quality=51
            )
            return mark_safe(
                f'<img src="{crop_img.url}" width=50>'
            )
        return 'Нет изображения'

    get_image_thumb.short_description = 'превью'
    get_image_thumb.allow_tags = True

    class Meta:
        verbose_name_plural = 'товары'
        verbose_name = 'товар'

    def __str__(self):
        return core.utils.remove_html_tags(self.text)


class Image(core.models.AbstractImage):
    item = django.db.models.OneToOneField(
        to=Item,
        on_delete=django.db.models.deletion.CASCADE,
        related_name='main_image',
        verbose_name='товар'
    )


class Gallery(core.models.AbstractImage):
    item = django.db.models.ForeignKey(
        to=Item,
        on_delete=django.db.models.deletion.CASCADE,
        related_name='gallery',
        verbose_name='товар'
    )

    def __str__(self):
        return self.image.url
