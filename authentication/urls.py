"""
Authentication app URL configuration.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    # AllAuth URLs will be included
]