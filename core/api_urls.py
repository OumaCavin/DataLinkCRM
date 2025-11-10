"""
Core API URL configuration.
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# API endpoints will be added here
# router = DefaultRouter()
# router.register(r'customers', views.CustomerViewSet)
# router.register(r'projects', views.ProjectViewSet)

urlpatterns = [
    # JWT Authentication
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API v1 endpoints
    # path('', include(router.urls)),
]