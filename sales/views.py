from django.shortcuts import render
# from .models import Sale
from salesItems.models import SalesItems
import datetime
from stocks.models import Stock
from orders.models import Orders,Sale

# Create your views here.


def invoice(request):
    print('invoice')
    data = request.GET.all()
    invoice_No = datetime.datetime.now().strftime("%S%M%H%d%m%Y")
    Sale(invoice_no= invoice_No, total_quantity=data.total_quantity, discount=0, total_price=data.total_price, status='COMPLETED').save()
    SalesItems(invoice_no= invoice_No, stock_id=data.stock_id, name=data.name, quantity=data.quantity, sale_price=data.sale_price).save()
    for d in data:
        stock = Stock.objects.get(stock_id = d.stock_id)
        updatedQuantity =stock.quantity-d.quantity
        Stock.objects.filter(stock_id = d.stock_id).update(quantity = updatedQuantity)
    Orders.objects.all().delete()
    msg='Data '
    return render(request, 'home.html')
 
