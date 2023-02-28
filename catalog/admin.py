import catalog.models

import django.contrib.admin


class ImageInline(django.contrib.admin.TabularInline):
    model = catalog.models.Image


class GalleryInline(django.contrib.admin.TabularInline):
    model = catalog.models.Gallery


@django.contrib.admin.register(catalog.models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.get_image_thumb
    )
    list_editable = (
        catalog.models.Item.is_published.field.name,
    )
    filter_horizontal = (
        'tags',
    )
    inlines = (
        ImageInline,
        GalleryInline
    )


@django.contrib.admin.register(catalog.models.Category)
class CategoryAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Category.name.field.name,
        catalog.models.Category.is_published.field.name,
    )
    list_editable = (
        catalog.models.Category.is_published.field.name,
    )


@django.contrib.admin.register(catalog.models.Tag)
class TagAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Tag.name.field.name,
        catalog.models.Tag.is_published.field.name,
    )
    list_editable = (
        catalog.models.Tag.is_published.field.name,
    )
