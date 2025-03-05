from django.db import models

class Shipment(models.Model):
    order_id = models.IntegerField(unique=True)
    user_id = models.IntegerField()
    address = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled')
    ], default='pending')
    tracking_number = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
