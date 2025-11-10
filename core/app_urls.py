"""
Core app URL configuration.
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard-redirect/', views.DashboardRedirectView.as_view(), name='dashboard-redirect'),
]