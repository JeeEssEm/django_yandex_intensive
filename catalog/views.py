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
            queryset=models.Tag.objects.filter(is_published=True)
        )
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
    for it in items:
        print(it)
    return render(request, template, context)


def item_detail(request, el):
    template = 'catalog/item_page.html'
    item = get_object_or_404(
        models.Item,
        pk=el
    )
    context = {
        'item': item
    }

    return render(request, template, context)


def positive_integer(request, pk):
    return HttpResponse(f'<body>{pk}</body>')
