from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    productname = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', max_length=5000, null=True, blank=True)
    quantity = models.IntegerField(default=0)


class TempMyOrder(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    productname = models.CharField(max_length=200, null=True)
    money =models.CharField(max_length=200, null=True)
    quantity = models.IntegerField(default=0)
# productname = models.CharField(max_length=200, null=True)

# Main Data
class UserData(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    productname = models.CharField(max_length=200, null=True)
    money = models.CharField(max_length=200, null=True)
    transactionid = models.CharField(max_length=200, null=True)


class TotalNumber(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    answer = models.CharField(max_length=200, null=True) 


class CartNumber(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    count = models.CharField(max_length=200, null=True) 


