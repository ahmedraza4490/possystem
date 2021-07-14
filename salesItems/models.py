from django.db import models

from orders.models import Orders

class SalesItems(models.Model):
    invoice_no = models.CharField(max_length=30,default=None)
    stock_id = models.CharField(max_length=14,default=None)
    name =  models.CharField(max_length=30, default=None)
    quantity =  models.IntegerField(default=0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=None)