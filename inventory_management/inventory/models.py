from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    stock = models.IntegerField()
    stock_alert_threshold = models.IntegerField(default=10)
    barcode = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class UserAccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_time = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)
