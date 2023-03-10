from django.urls import path, re_path, register_converter

from . import converters, views

register_converter(converters.PositiveIntegerConverter, 'positive_int')

app_name = 'catalog'

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('<int:el>', views.item_detail, name='item_detail'),
    re_path(r'^re/(?P<pk>[1-9]\d*)$', views.positive_integer),
    path('converter/<positive_int:pk>', views.positive_integer),
    path('test', views.new_items, name='new_items'),
    path('changes', views.no_changes, name='new_items'),
]
