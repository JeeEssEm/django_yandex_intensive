from catalog import models

import django.db.models


class ItemManager(django.db.models.Manager):
    def published(self):
        return self.get_queryset().filter(
            is_published=True,
            category__is_published=True
        ).prefetch_related(
            django.db.models.Prefetch(
                'tags',
                queryset=models.Tag.objects.filter(
                    is_published=True
                ).only('name')
            ),
        ).select_related(
            'category',
            'main_image'
        ).only(
            'id',
            'name',
            'text',
            'category__name',
            'main_image__image',
        )

    def homepage(self):
        return self.published().filter(is_on_main=True).order_by('name')

    def catalog(self):
        return self.published().order_by('category__name')

    def detail(self, el):
        return self.published().prefetch_related('gallery').filter(pk=el)
