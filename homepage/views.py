from django.http import HttpResponse
from http import HTTPStatus


def home(request):
    return HttpResponse('<body><h1>Главная</h1></body>')


def coffee(request):
    return HttpResponse(
        '<body>Я чайник</body>',
        status=HTTPStatus.IM_A_TEAPOT)
