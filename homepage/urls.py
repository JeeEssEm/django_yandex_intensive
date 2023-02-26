from django.urls import path

from . import views

app_name = 'homepage'

urlpatterns = [
    path('coffee/', views.coffee),
    path('', views.home, name='home'),
]
