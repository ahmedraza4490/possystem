from django.db import models
from rest_framework import serializers

# Create your models here.

CATEGORIES = (
    ('softdrinks','SOFTDRINKS'),
    ('snacks', 'SNACKS'),
    ('miscallaneous','Miscallaneous'),
)

class Orders(models.Model):
    stock_id         = models.CharField(max_length=14)
    name             =  models.CharField(max_length=30)
    category         =  models.CharField(max_length=15, choices=CATEGORIES, default='miscallaneous')
    quantity         =  models.IntegerField(default=0)
    sale_price       =  models.DecimalField(max_digits=10, decimal_places=2)


class OrderSerializer(serializers.Serializer):
    stock_id = serializers.CharField(max_length=14)
    name = serializers.CharField(max_length=30)
    category = serializers.CharField(max_length=15)
    quantity = serializers.CharField()
    sale_price = serializers.IntegerField()
    id = serializers.IntegerField()


class Sale(models.Model):
    invoice_id       =  models.AutoField(primary_key=True)
    discount         =  models.IntegerField()
    total      =  models.DecimalField(max_digits=10, decimal_places=2)
    sub_total   =  models.CharField(max_length=10)
    products =   models.JSONField()
    selesDate = models.DateTimeField(auto_now=True)
    month = models.IntegerField()
    year = models.IntegerField()