from django.urls import path

from . import views

urlpatterns = [
    path('coffee/', views.coffee),
    path('', views.home),
]
