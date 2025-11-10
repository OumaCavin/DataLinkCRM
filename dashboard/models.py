"""
Dashboard models for DataLinkCRM.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class DashboardWidget(models.Model):
    """Custom dashboard widgets."""
    WIDGET_TYPES = [
        ('chart', 'Chart'),
        ('metric', 'Metric'),
        ('table', 'Table'),
        ('map', 'Map'),
        ('calendar', 'Calendar'),
        ('list', 'List'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    description = models.TextField(blank=True)
    configuration = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    position = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_widgets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['position', 'name']
        verbose_name = 'Dashboard Widget'
        verbose_name_plural = 'Dashboard Widgets'
    
    def __str__(self):
        return f"{self.name} ({self.get_widget_type_display()})"

class SystemStats(models.Model):
    """System statistics for dashboard."""
    date = models.DateField(unique=True, default=timezone.now)
    total_customers = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_projects = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, validators=[MinValueValidator(0)])
    active_subscriptions = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    new_customers_today = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    projects_completed = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    payment_success_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    average_response_time = models.FloatField(default=0.0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'System Statistic'
        verbose_name_plural = 'System Statistics'
    
    def __str__(self):
        return f"Stats for {self.date}"

class QuickAction(models.Model):
    """Quick action shortcuts for dashboard."""
    ICON_CHOICES = [
        ('fas fa-user-plus', 'Add Customer'),
        ('fas fa-project-diagram', 'New Project'),
        ('fas fa-credit-card', 'Process Payment'),
        ('fas fa-envelope', 'Send Email'),
        ('fas fa-calendar-plus', 'Schedule Meeting'),
        ('fas fa-file-invoice-dollar', 'Create Invoice'),
        ('fas fa-chart-line', 'View Reports'),
        ('fas fa-cog', 'System Settings'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, choices=ICON_CHOICES)
    url = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    position = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quick_actions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['position', 'name']
        verbose_name = 'Quick Action'
        verbose_name_plural = 'Quick Actions'
    
    def __str__(self):
        return self.name

class Notification(models.Model):
    """System notifications for users."""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    message = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    action_url = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    @property
    def time_since_created(self):
        """Return time since creation in human readable format."""
        import datetime
        now = timezone.now()
        diff = now - self.created_at
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return "Just now"
