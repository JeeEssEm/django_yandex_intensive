from catalog import models

from datetime import date, timedelta

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
import django.db.models


def item_list(request):
    template = 'catalog/item_list.html'
    items = models.Item.objects.catalog()

    context = {
        'items': items,
        'title': 'Страница с товарами'
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
    template = 'catalog/item_list.html'
    delta = date.today() - timedelta(days=7)

    items = models.Item.objects.published().filter(
        created_at__gte=delta
    )

    context = {
        'items': items,
        'title': 'Новинки'
    }

    return render(request, template, context)


def friday(request):
    template = 'catalog/item_list.html'

    items = models.Item.objects.published().filter(
        created_at__iso_week_day=5
    ).order_by('-updated_at')[:5]

    context = {
        'items': items,
        'title': 'Пятница'
    }

    return render(request, template, context)


def no_changes(request):
    template = 'catalog/item_list.html'

    items = models.Item.objects.published().filter(
        created_at__date=django.db.models.F('updated_at__date'),
        created_at__hour=django.db.models.F('updated_at__hour'),
        created_at__minute=django.db.models.F('updated_at__minute'),
        created_at__second=django.db.models.F('updated_at__second')
    )

    context = {
        'items': items,
        'title': 'Непроверенное'
    }

    return render(request, template, context)

