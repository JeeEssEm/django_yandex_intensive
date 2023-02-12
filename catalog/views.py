from django.http import HttpResponse


def item_list(request):
    return HttpResponse('<body>Список элементов</body>')


def item_detail(request, el):
    return HttpResponse(f'<body>Подробно элемент {el}</body>')
