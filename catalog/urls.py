from django.urls import path, re_path, register_converter

from . import views, converters


register_converter(converters.PositiveIntegerConverter, 'positive_int')

urlpatterns = [
    path('', views.item_list),
    path('<int:el>', views.item_detail),
    re_path(r'^re/([1-9]\d*)$', views.positive_integer),
    path('converter/<positive_int:number>', views.positive_integer),
]
