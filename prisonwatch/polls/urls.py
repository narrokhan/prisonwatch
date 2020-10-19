from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('remove_all_bbsnews', views.remove_all_bbsnews, name='remove_all_bbsnews'),
]
