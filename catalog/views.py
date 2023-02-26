from django.http import HttpResponse
from django.shortcuts import render


def item_list(request):
    template = 'catalog/item_list.html'
    context = {
        'items': list(range(1, 11))
    }
    return render(request, template, context)


def item_detail(request, el):
    return HttpResponse(f'<body>detailed about {el}</body>')


def positive_integer(request, pk):
    return HttpResponse(f'<body>{pk}</body>')
