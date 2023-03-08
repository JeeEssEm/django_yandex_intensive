from http import HTTPStatus

from catalog import models

import django.db.models
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    template = 'homepage/home.html'
    items = models.Item.objects.filter(
        is_on_main=True,
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
    ).order_by('name')

    context = {
        'items': items
    }
    return render(request, template, context)


def coffee(request):
    return HttpResponse(
        '<body>Я чайник</body>',
        status=HTTPStatus.IM_A_TEAPOT)
