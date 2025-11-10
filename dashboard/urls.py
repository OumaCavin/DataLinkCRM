"""
Dashboard app URL configuration.
"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_index, name='index'),
    path('analytics/', views.DashboardAnalyticsView.as_view(), name='analytics'),
    path('api/dashboard-data/', views.get_dashboard_data, name='dashboard-data'),
    path('notifications/<uuid:notification_id>/mark-read/', views.mark_notification_read, name='mark-notification-read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark-all-notifications-read'),
    path('widgets/<uuid:widget_id>/data/', views.widget_data, name='widget-data'),
]