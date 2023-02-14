from django.http import HttpResponse


def home(request):
    return HttpResponse('<body><h1>Главная</h1></body>')


def coffee(request):
    return HttpResponse('<body>Я чайник</body>', status=418)
