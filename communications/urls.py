"""
Communications app URL configuration.
"""
from django.urls import path
from . import views

app_name = 'communications'

urlpatterns = [
    path('', views.index, name='index'),
]