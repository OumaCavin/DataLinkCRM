"""
ScheduleCal app URL configuration.
"""
from django.urls import path
from . import views

app_name = 'schedulecal'

urlpatterns = [
    path('', views.index, name='index'),
]