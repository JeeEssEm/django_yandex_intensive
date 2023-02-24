from catalog import utils

import django.core.exceptions
import django.db.models


class AbstractItem(django.db.models.Model):
    name = django.db.models.CharField(
        'Название',
        help_text='Название, длина не более 150 символов',
        max_length=150
    )
    is_published = django.db.models.BooleanField(
        'Опубликовано',
        default=True
    )
    normalized_name = django.db.models.CharField(
        'Нормализованное имя',
        max_length=150,
        unique=True,
    )

    class Meta:
        abstract = True

    def save(self):
        self.normalized_name = utils.get_normalized(self.name)
        super().save()

    def validate_unique(self, exclude=None):
        self.normalized_name = utils.get_normalized(self.name)
        similar_obj = type(self).objects.filter(
            normalized_name=self.normalized_name
        ).first()

        if similar_obj is not None and similar_obj != self:
            raise django.core.exceptions.ValidationError({
                'name': 'Похожее имя уже существует'
                })

        return super().validate_unique(exclude)

    def __str__(self):
        return self.name


class AbstractName(django.db.models.Model):
    slug = django.db.models.SlugField(
        'Cлаг',
        help_text='Человекочитаемый формат URL',
        max_length=200,
        unique=True,
        validators=[
            django.core.validators.validate_slug,
        ]
    )

    class Meta:
        abstract = True
