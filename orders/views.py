from django.shortcuts import redirect, render
from stocks.models import Stock
from .models import Orders,OrderSerializer
from django.http import HttpResponse
import json
from pointofsales.views import home
from orders.models import Sale

# Create your views here.
def getItems(request):
    stockID = request.GET['id']
    print(stockID)
    datalist = list()
    StockItems = Stock.objects.get(stock_id = stockID)
    if Orders.objects.filter(stock_id = stockID):
        tempOrders = Orders.objects.get(stock_id = stockID)
        if StockItems.quantity > tempOrders.quantity:
            Orders.objects.filter(stock_id = stockID).update(quantity = tempOrders.quantity + 1)
        else:
            msg = 'Quantity equal'
    else:
        Orders(stock_id = stockID, name = StockItems.name, category = StockItems.category, quantity=1, sale_price=StockItems.sale_price).save()
    tblOrders = Orders.objects.all()
    for objOrders in tblOrders:
        datalist.append(OrderSerializer(objOrders).data) 
    return HttpResponse(json.dumps(datalist))


def add_ten_items(request):
    id = request.GET['id']
    print(f'id : {id}')
    my_list = []
    if Stock.objects.filter(stock_id = id).exists():
        obj = Stock.objects.get(stock_id = id)
        if obj.quantity >= 10:
            my_dict = {}
            my_dict['name'] = obj.name
            my_dict['code'] = str(obj.stock_id)
            my_dict['sale_price'] = str(obj.sale_price)
            my_dict['quantity'] = 10
            my_list.append(my_dict)
            data = 0
            try:
                # customer purchase more than one items
                data = request.session['purchases']
                product_exists = False
                for my_obj in data:
                    # product is already  exist in list. so this time wo will only increase quantity of product
                    if my_obj['name'] == obj.name:
                        my_obj['quantity'] = int(my_obj['quantity']) + 10
                        product_exists = True
                        # print('break loop')
                        break
                if product_exists == False:
                    # product is not  exist in bill list 
                    data.append(my_dict)
                request.session['purchases'] = data
            except:
                # this is first item added by customer
                data = my_list
                request.session['purchases'] = my_list
            return HttpResponse(json.dumps(data))
        else:
            print('less quantity')
            return HttpResponse(json.dumps(''))


def getItemByName(request):
    name = None
    code = request.GET['code']
    quantity = int(request.GET['quantity'])
    name = request.GET['name']
    print(f'name : {name} : code : {code} : quantity : {quantity} ')
    my_list = []
    stockList = None
    if code != '0':
        if Stock.objects.filter(stock_id = code).exists():
            stockList = Stock.objects.get(stock_id = code)
            name = stockList.name 
        else:
            return HttpResponse(json.dumps('No Item Found '))
    else:
        if Stock.objects.filter(name = name).exists():
            stockList = Stock.objects.get(name = name)
        else:
            return HttpResponse(json.dumps('No Item Found against this code'))

    if stockList.quantity <= quantity:
        return HttpResponse(json.dumps('Total Quantity left :' + stockList.quantity))
    else:
        my_dict = {}
        my_dict['name'] = stockList.name
        my_dict['code'] = str(stockList.stock_id)
        my_dict['sale_price'] = str(stockList.sale_price)
        my_dict['quantity'] = str(quantity)
        my_list.append(my_dict)
        data = 0
    try:
        # customer purchase more than one items
        data = request.session['purchases_']
        product_exists = False
        for my_obj in data:
            if my_obj['name'] == name:
                my_obj['quantity'] = int(my_obj['quantity']) + int(quantity)
                product_exists = True
                break
        if product_exists == False:
            data.append(my_dict)
        request.session['purchases'] = data
    except :
        # this is first item added by customer
        data = my_list
        request.session['purchases'] = my_list
    return HttpResponse(json.dumps(data))

# def add_item(request):
#     print('add_item enter')
#     name = request.GET['name']
#     print(f'name : {name}')




def increase_quantity(request):
    print('increase_quantity enter')
    code = request.GET['code']
    print(f'code : {code}')
    stock_obj = Stock.objects.get(stock_id = code)
    name = stock_obj.name
    print(f'name : {name}')
    data = request.session['purchases']
    for obj in data:
        if obj['name'] == name:
            print('name matched')
            obj['quantity'] = int(obj['quantity']) + 1
            print('break loop')
            break
    request.session['purchases'] = data
    # item_name = {}
    # item_name['name'] = name
    data.append(name)
    print(data)
    return HttpResponse(json.dumps(name))


def add_item(request):
    print('add_item enter')
    name = request.GET['name']
    print(f'name : {name}')
    data = request.session['purchases']
    for obj in data:
        if obj['name'] == name:
            print('name matched')
            obj['quantity'] = int(obj['quantity']) + 1
            print('break loop')
            break
    request.session['purchases'] = data
    print(data)
    return HttpResponse(json.dumps(name))

def subtract_item(request):
    name = request.GET['name']
    print(f'name : {name}')
    data = request.session['purchases']
    for obj in data:
        if obj['name'] == name:
            if int(obj['quantity']) > 0:
                obj['quantity'] = int(obj['quantity']) - 1
                print('break loop')
                break
    request.session['purchases'] = data
    print(data)
    return HttpResponse(json.dumps(name))


def save_discount(request):
    discount = request.GET['my_discount']
    print(f'discount : {discount}')
    request.session['discount'] = discount
    return HttpResponse()


def delete_item(request):
    name = request.GET['name']
    print(f'name : {name}')
    data = request.session['purchases']
    my_list = []
    for obj in data:
        if obj['name'] == name:
            print('found')
        else:
            my_list.append(obj)
    # request.session['purchases'] = my_list
    print(my_list)
    return HttpResponse(json.dumps(name))

def deleteItem(request):
    try:
        order = Orders.objects.get(id = request.GET['id'])
        order.delete()
        return HttpResponse('true')
    except:
        return HttpResponse('false')



from datetime import datetime
def create_order(request):
    order = request.session['purchases']
    currentYear = datetime.now().year
    currentMonth = datetime.now().month
    print(f'orders : {order}')
    my_list = []
    total = 0
    for data in order:
        my_dict = {}
        my_dict['name'] = data['name']
        my_dict['code'] = str(data['code'])
        my_dict['sale_price'] = str(data['sale_price'])
        my_dict['quantity'] = str(data['quantity'])
        my_dict['total'] = float(data['sale_price']) * int(data['quantity'])
        total += int(data['quantity']) * float(data['sale_price'])
        my_list.append(my_dict)
    json_data = json.dumps(my_list)
    Sale(total = total, products = json_data, sub_total=total , discount=0, month =currentMonth,year = currentYear ).save()
    stock = Stock.objects.all()
    for data in order:
        stock_obj = stock.get(name = data['name'])
        new_quantity = stock_obj.quantity - int(data['quantity'])
        Stock.objects.filter(name = data['name']).update(quantity = new_quantity)
    return redirect(home)