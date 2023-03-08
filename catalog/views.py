from catalog import models

import django.db.models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render


def item_list(request):
    template = 'catalog/item_list.html'
    items = models.Item.objects.filter(
        is_published=True,
        category__is_published=True
    ).prefetch_related(
        django.db.models.Prefetch(
            'tags',
            queryset=models.Tag.objects.filter(is_published=True).only('name')
        ),
        'gallery',
    ).select_related(
        'category',
        'main_image'
    ).only(
        'id',
        'name',
        'text',
        'category__name',
        'main_image__image',
    ).order_by('category__name')

    context = {
        'items': items
    }

    return render(request, template, context)


def item_detail(request, el):
    template = 'catalog/item_page.html'
    query_item = models.Item.objects.filter(
        pk=el,
        category__is_published=True,
        is_published=True
    ).select_related(
        'category',
        'main_image'
    ).prefetch_related(
        'tags',
        'gallery'
    ).only(
        'name',
        'text',
        'category__name',
        'main_image__image'
    )

    item = get_object_or_404(
        query_item
    )
    context = {
        'item': item
    }

    return render(request, template, context)


def positive_integer(request, pk):
    return HttpResponse(f'<body>{pk}</body>')
