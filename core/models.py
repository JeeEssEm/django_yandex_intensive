import django.core.validators
import django.db.models

from sorl.thumbnail import ImageField


class AbstractItem(django.db.models.Model):
    name = django.db.models.CharField(
        'название',
        help_text='Название, длина не более 150 символов',
        max_length=150
    )
    is_published = django.db.models.BooleanField(
        'опубликовано',
        default=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class AbstractName(django.db.models.Model):
    slug = django.db.models.SlugField(
        'слаг',
        help_text='Человекочитаемый формат URL',
        max_length=200,
        unique=True,
        validators=[
            django.core.validators.validate_slug,
        ]
    )

    class Meta:
        abstract = True


class AbstractImage(django.db.models.Model):
    image = ImageField(
        'прикрепите изображение',
        upload_to='catalog/',
    )

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'
        abstract = True

    def __str__(self):
        return self.image.url
