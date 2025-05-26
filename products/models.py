from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    prices = models.JSONField(default=list)
    
    def __str__(self):
        return self.name

class AvailableProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='availability')
    quantity_in_ml = models.IntegerField()
    date = models.DateField(auto_now=True)
    
    class Meta:
        unique_together = ['product', 'date']
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity_in_ml}ml"
