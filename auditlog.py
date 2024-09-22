# Audit trail

from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Sale, AuditTrail
from django.utils.timezone import now

@receiver(pre_save, sender=Sale)
def audit_sale_update(sender, instance, **kwargs):
    if instance.id:  # Existing sale is being updated
        old_sale = Sale.objects.get(pk=instance.id)
        if old_sale.quantity_sold != instance.quantity_sold or old_sale.total_price != instance.total_price:
            AuditTrail.objects.create(
                user=instance.attendant,
                action='UPDATE',
                model='Sale',
                object_id=instance.id,
                old_data={'quantity_sold': old_sale.quantity_sold, 'total_price': old_sale.total_price},
                new_data={'quantity_sold': instance.quantity_sold, 'total_price': instance.total_price},
                timestamp=now()
            )

@receiver(post_delete, sender=Sale)
def audit_sale_delete(sender, instance, **kwargs):
    AuditTrail.objects.create(
        user=instance.attendant,
        action='DELETE',
        model='Sale',
        object_id=instance.id,
        old_data={'quantity_sold': instance.quantity_sold, 'total_price': instance.total_price},
        timestamp=now()
    )


# auditTrail model
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.postgres.fields import JSONField  # Use JSONField for Postgres

class AuditTrail(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model = models.CharField(max_length=50)  # The name of the model being affected
    object_id = models.PositiveIntegerField()  # ID of the affected object
    old_data = JSONField(null=True, blank=True)  # Data before the change (if applicable)
    new_data = JSONField(null=True, blank=True)  # Data after the change (if applicable)
    timestamp = models.DateTimeField(default=now)
    
    def __str__(self):
        return f'{self.action} on {self.model} by {self.user} at {self.timestamp}'

# Tracking action  using 'Signal'
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    AuditTrail.objects.create(
        user=user,
        action='LOGIN',
        model='User',
        object_id=user.id,
        timestamp=now()
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    AuditTrail.objects.create(
        user=user,
        action='LOGOUT',
        model='User',
        object_id=user.id,
        timestamp=now()
    )

# using external lib
pip install django-simple-history

# add model 'sale'
from simple_history.models import HistoricalRecords

class Sale(models.Model):
    attendant = models.ForeignKey(User, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    fuel_type = models.CharField(max_length=50)
    quantity_sold = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_time = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()  # Enable auditing for this model


sale = Sale.objects.get(id=1)
sale.history.all()  # Retrieve all historical records for this sale

pip install django-reversion
import reversion
from django.db import models

class Inventory(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    fuel_type = models.CharField(max_length=50)
    opening_level = models.DecimalField(max_digits=10, decimal_places=2)
    closing_level = models.DecimalField(max_digits=10, decimal_places=2)

reversion.register(Inventory)  # Enable version control
# saving version
with reversion.create_revision():
    instance.save()

# reverting changes
previous_version = reversion.get_for_object(instance).first()
previous_version.revision.comment
