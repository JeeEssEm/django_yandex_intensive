from django.http import HttpResponse
from django.shortcuts import render


def item_list(request):
    template = 'catalog/item_list.html'
    context = {
        'items': list(range(1, 11))
    }
    return render(request, template, context)


def item_detail(request, el):
    template = 'catalog/item_page.html'
    context = {
        'item': el
    }
    return render(request, template, context)


def positive_integer(request, pk):
    return HttpResponse(f'<body>{pk}</body>')
