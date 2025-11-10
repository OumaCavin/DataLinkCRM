"""
Customer models for DataLinkCRM.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import uuid

class Customer(models.Model):
    """Customer model for CRM."""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    CUSTOMER_TYPES = [
        ('individual', 'Individual'),
        ('business', 'Business'),
        ('organization', 'Organization'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('prospect', 'Prospect'),
        ('lead', 'Lead'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
    customer_id = models.CharField(max_length=20, unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\+254[0-9]{9}$',
            message='Phone number must be in format +254XXXXXXXXX'
        )]
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES, default='individual')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='prospect')
    
    # Address information
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Kenya')
    postal_code = models.CharField(max_length=10, blank=True)
    
    # Business information
    company_name = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    
    # Additional information
    date_of_birth = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    tags = models.CharField(max_length=500, blank=True, help_text='Comma-separated tags')
    is_primary_contact = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_contacted = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
            models.Index(fields=['status']),
            models.Index(fields=['customer_type']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.customer_id})"
    
    def get_full_name(self):
        """Return the customer's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def name(self):
        """Return the customer's name."""
        return self.get_full_name()
    
    def save(self, *args, **kwargs):
        if not self.customer_id:
            # Generate customer ID
            import random
            import string
            self.customer_id = f"CUS{random.randint(100000, 999999)}"
        super().save(*args, **kwargs)

class CustomerNote(models.Model):
    """Customer notes."""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Customer Note'
        verbose_name_plural = 'Customer Notes'
    
    def __str__(self):
        return f"Note for {self.customer.name} by {self.user.username}"

class CustomerInteraction(models.Model):
    """Customer interaction tracking."""
    INTERACTION_TYPES = [
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('sms', 'SMS'),
        ('chat', 'Chat'),
        ('visit', 'Visit'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='interactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    interaction_date = models.DateTimeField(default=models.DateTimeField)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    outcome = models.CharField(max_length=100, blank=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-interaction_date']
        verbose_name = 'Customer Interaction'
        verbose_name_plural = 'Customer Interactions'
    
    def __str__(self):
        return f"{self.customer.name} - {self.get_interaction_type_display()}"
