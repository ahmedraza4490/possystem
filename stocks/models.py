from calendar import month
from django.db import models
import datetime
from orders.models import Sale

CATEGORIES = (
    ('softdrinks','SOFTDRINKS'),
    ('snacks', 'SNACKS'),
    ('miscallaneous','Miscallaneous'),
)
class Stock(models.Model):
    stock_id         = models.CharField(max_length=14,primary_key=True, default= datetime.datetime.now().strftime("%S%M%H%d%m%Y") , editable=False)
    name             =  models.CharField(max_length=30)
    category         =  models.CharField(max_length=15, choices=CATEGORIES, default='miscallaneous')
    quantity         =  models.IntegerField()
    vendors          =  models.CharField(max_length=35)
    sale_price       =  models.DecimalField(max_digits=10, decimal_places=2)
    cost_price       =  models.DecimalField(max_digits=10, decimal_places=2)
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['stock_id','category','quantity','vendors','sale_price','cost_price']
    def __str__(self):
        return self.name


class Vendor(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    company = models.CharField(max_length=30)


class Return(models.Model):
    return_id = models.AutoField(primary_key=True)
    invoice_id = models.ForeignKey(Sale, on_delete=models.CASCADE)
    return_list = models.JSONField()
    amount = models.IntegerField()
    date=models.DateTimeField(default='2021-07-06 14:39:50.140839+05',null=True)
    month = models.IntegerField()
    year = models.IntegerField()