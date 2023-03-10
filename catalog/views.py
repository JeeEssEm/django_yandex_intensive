from catalog import models

from datetime import date, timedelta

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
import django.db.models


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


def new_items(request):
    template = 'includes/items_template.html'
    delta = date.today() - timedelta(days=7)

    items = models.Item.objects.published().filter(
        created_at__gte=delta
    )

    context = {
        'items': items
    }
    print(items)

    return render(request, template, context)


def friday(request):
    template = 'includes/items_template.html'
    delta = date.today() - timedelta(days=7)

    items = models.Item.objects.published().filter(
        created_at__gte=delta
    )

    context = {
        'items': items
    }
    print(items)

    return render(request, template, context)


def no_changes(request):
    template = 'includes/items_template.html'

    items = models.Item.objects.published().filter(
        created_at=django.db.models.F('updated_at')
    )

    context = {
        'items': items
    }
    print(items)

    return render(request, template, context)

