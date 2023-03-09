from catalog import models

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render


def item_list(request):
    template = 'catalog/item_list.html'
    items = models.Item.objects.catalog()

    context = {
        'items': items
    }

    return render(request, template, context)


def item_detail(request, el):
    template = 'catalog/item_page.html'
    query_item = models.Item.objects.detail(el)

    item = get_object_or_404(
        query_item
    )
    context = {
        'item': item
    }

    return render(request, template, context)


def positive_integer(request, pk):
    return HttpResponse(f'<body>{pk}</body>')
