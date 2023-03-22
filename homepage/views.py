from http import HTTPStatus


from catalog import models

from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    template = 'homepage/home.html'
    items = models.Item.objects.homepage()

    context = {
        'items': items
    }
    return render(request, template, context)


def coffee(request):
    if request.user.is_authenticated:
        request.user.profile.coffee_count += 1
        request.user.profile.save()

    return HttpResponse(
        '<body>Я чайник</body>',
        status=HTTPStatus.IM_A_TEAPOT)
