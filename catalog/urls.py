from django.urls import path, re_path, register_converter

from . import converters, views

register_converter(converters.PositiveIntegerConverter, 'positive_int')

urlpatterns = [
    path('', views.item_list),
    path('<int:el>', views.item_detail),
    re_path(r'^re/(?P<pk>[1-9]\d*)$', views.positive_integer),
    path('converter/<positive_int:pk>', views.positive_integer),
]
