from django.db import models

class Cart(models.Model):
    user_id = models.IntegerField() 
    product_id = models.CharField(max_length=255) 
    product_type = models.CharField(max_length=50)  
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('user_id', 'product_id', 'product_type')

    def __str__(self):
        return f"User {self.user_id} - Product {self.product_id}"
