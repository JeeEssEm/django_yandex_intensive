import django.core.validators
import django.db.models


class AbstractItem(django.db.models.Model):
    name = django.db.models.CharField(
        'Название',
        max_length=150
    )
    is_published = django.db.models.BooleanField(
        'Опубликовано',
        default=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class AbstractName(django.db.models.Model):
    slug = django.db.models.CharField(
        'Cлаг',
        max_length=200,
        unique=True,
        validators=[
            django.core.validators.validate_slug,
        ]
    )

    class Meta:
        abstract = True
