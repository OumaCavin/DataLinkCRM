"""
Dashboard views for DataLinkCRM.
Comprehensive dashboard with widgets, analytics, and quick actions.
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
import json
import datetime

from .models import DashboardWidget, SystemStats, QuickAction, Notification
from customers.models import Customer
from projects.models import Project
from payments.models import Payment
from subscriptions.models import Subscription

@login_required
def dashboard_index(request):
    """Main dashboard view with comprehensive overview."""
    
    # Get system statistics
    try:
        latest_stats = SystemStats.objects.latest('date')
    except SystemStats.DoesNotExist:
        # Create default stats if none exist
        latest_stats = SystemStats.objects.create(
            total_customers=0,
            total_projects=0,
            total_revenue=0.00,
            active_subscriptions=0
        )
    
    # Get user's custom widgets
    user_widgets = DashboardWidget.objects.filter(
        user=request.user, 
        is_active=True
    ).order_by('position')
    
    # Get user's quick actions
    quick_actions = QuickAction.objects.filter(
        user=request.user, 
        is_active=True
    ).order_by('position')[:8]
    
    # Get recent notifications
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]
    
    # Unread notifications count
    unread_count = notifications.filter(is_read=False).count()
    
    # Recent activity data
    recent_customers = Customer.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]
    
    recent_projects = Project.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]
    
    recent_payments = Payment.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]
    
    # Calculate additional metrics
    current_month = timezone.now().replace(day=1)
    month_customers = Customer.objects.filter(
        user=request.user,
        created_at__gte=current_month
    ).count()
    
    month_revenue = Payment.objects.filter(
        user=request.user,
        status='completed',
        created_at__gte=current_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    active_projects = Project.objects.filter(
        user=request.user,
        status__in=['in_progress', 'planning']
    ).count()
    
    context = {
        'title': 'Dashboard',
        'stats': latest_stats,
        'user_widgets': user_widgets,
        'quick_actions': quick_actions,
        'notifications': notifications,
        'unread_count': unread_count,
        'recent_customers': recent_customers,
        'recent_projects': recent_projects,
        'recent_payments': recent_payments,
        'month_customers': month_customers,
        'month_revenue': month_revenue,
        'active_projects': active_projects,
        'current_date': timezone.now(),
    }
    
    return render(request, 'dashboard/index.html', context)

@login_required
@require_http_methods(["GET"])
def get_dashboard_data(request):
    """API endpoint to get dashboard data in JSON format."""
    
    # Get statistics
    try:
        latest_stats = SystemStats.objects.latest('date')
    except SystemStats.DoesNotExist:
        latest_stats = None
    
    # Recent activity
    recent_customers = Customer.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]
    
    recent_projects = Project.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]
    
    recent_payments = Payment.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]
    
    # Unread notifications
    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()
    
    data = {
        'stats': {
            'total_customers': latest_stats.total_customers if latest_stats else 0,
            'total_projects': latest_stats.total_projects if latest_stats else 0,
            'total_revenue': float(latest_stats.total_revenue) if latest_stats else 0,
            'active_subscriptions': latest_stats.active_subscriptions if latest_stats else 0,
        },
        'recent_customers': [
            {
                'id': customer.id,
                'name': customer.get_full_name(),
                'email': customer.email,
                'created_at': customer.created_at.isoformat(),
            }
            for customer in recent_customers
        ],
        'recent_projects': [
            {
                'id': project.id,
                'name': project.name,
                'status': project.get_status_display(),
                'created_at': project.created_at.isoformat(),
            }
            for project in recent_projects
        ],
        'recent_payments': [
            {
                'id': payment.id,
                'amount': float(payment.amount),
                'status': payment.get_status_display(),
                'method': payment.get_payment_method_display(),
                'created_at': payment.created_at.isoformat(),
            }
            for payment in recent_payments
        ],
        'unread_notifications': unread_notifications,
        'last_updated': timezone.now().isoformat(),
    }
    
    return JsonResponse(data)

@login_required
@require_http_methods(["POST"])
def mark_notification_read(request, notification_id):
    """Mark a notification as read."""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    
    return JsonResponse({
        'success': True,
        'message': 'Notification marked as read'
    })

@login_required
@require_http_methods(["POST"])
def mark_all_notifications_read(request):
    """Mark all notifications as read."""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    return JsonResponse({
        'success': True,
        'message': 'All notifications marked as read'
    })

@login_required
@require_http_methods(["GET"])
def widget_data(request, widget_id):
    """Get data for a specific widget."""
    widget = get_object_or_404(DashboardWidget, id=widget_id, user=request.user)
    
    # This would be expanded based on widget type
    widget_data = {
        'id': str(widget.id),
        'name': widget.name,
        'type': widget.widget_type,
        'data': widget.configuration,
        'created_at': widget.created_at.isoformat(),
    }
    
    return JsonResponse(widget_data)

class DashboardAnalyticsView(TemplateView):
    """Dashboard analytics view with advanced charts and metrics."""
    template_name = 'dashboard/analytics.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Time period filter (default to last 30 days)
        days = int(self.request.GET.get('days', 30))
        start_date = timezone.now() - datetime.timedelta(days=days)
        
        # Customer analytics
        customers_over_time = Customer.objects.filter(
            user=self.request.user,
            created_at__gte=start_date
        ).extra(
            select={'day': 'date(created_at)'}
        ).values('day').annotate(
            count=Count('id')
        ).order_by('day')
        
        # Revenue analytics
        revenue_over_time = Payment.objects.filter(
            user=self.request.user,
            status='completed',
            created_at__gte=start_date
        ).extra(
            select={'day': 'date(created_at)'}
        ).values('day').annotate(
            total=Sum('amount')
        ).order_by('day')
        
        # Project status distribution
        project_status_dist = Project.objects.filter(
            user=self.request.user
        ).values('status').annotate(
            count=Count('id')
        )
        
        # Payment method distribution
        payment_method_dist = Payment.objects.filter(
            user=self.request.user
        ).values('payment_method').annotate(
            count=Count('id')
        )
        
        context.update({
            'title': 'Analytics',
            'days': days,
            'customers_over_time': list(customers_over_time),
            'revenue_over_time': list(revenue_over_time),
            'project_status_dist': list(project_status_dist),
            'payment_method_dist': list(payment_method_dist),
        })
        
        return context
