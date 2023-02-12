from django.urls import path

from . import views

urlpatterns = [
    path('', views.item_list),
    path('<int:el>', views.item_detail),
]
