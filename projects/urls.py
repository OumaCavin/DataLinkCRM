"""
Projects app URL configuration.
"""
from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.index, name='index'),
    path('<uuid:project_id>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
]