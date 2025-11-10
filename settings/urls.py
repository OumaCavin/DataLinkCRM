"""
Settings app URL configuration.
"""
from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('quick-actions/', views.quick_actions, name='quick-actions'),
    path('notifications/', views.notifications, name='notifications'),
    path('widgets/', views.widgets, name='widgets'),
]