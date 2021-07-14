import json
from os import name
import re
from django.shortcuts import redirect, render
from stocks.models import Stock,Vendor,Return
from django.http import HttpResponse, HttpResponseRedirect
import calendar
from orders.models import Sale
from django.http import HttpResponse
from django.template.loader import get_template
from io import StringIO, BytesIO
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
import datetime as dated


# def inventory(request):
#     data = Stock.objects.all()
#     return render(request,'editinventory.html',{'data':data})

def returnProduct(request):
    return render(request,'returnProduct.html')

# def make_bill(request):
#     purchase = request.session['purchases']
#     bill = 0
#     d = 0
#     for data in purchase:
#         quantity = data['quantity']
#         sale_price = data['sale_price']
#         bill += int(quantity) * float(sale_price)
#         print(f' one : {bill}' )
        
#     return HttpResponse(json.dumps(bill))
    

def inventory(request):
 
    all_stock_Items = Stock.objects.all().order_by('stock_id')
 
    page_number = request.GET.get('page')

    return render(request, 'editinventory1.html', {'data':all_stock_Items})

def insertItem(request):
    vendor_obj = Vendor.objects.all()
    return render(request, 'insertitem.html',{'vendor_obj':vendor_obj})

def deleteItem(request):
    stockID = request.GET['id']
    Stock.objects.filter(stock_id = stockID).delete()
    return HttpResponseRedirect('inventory')

def insertData(request):
    print('Test')
    msg = ""
    if request.method == 'POST':
        stockID = request.POST['itemcode']
        item_name = request.POST['itemName']
        category = request.POST['category']
        quantity = request.POST['quantity']
        vendors = request.POST['DistributorName']
        sale_price = request.POST['salePrice']
        cost_price = request.POST['costPrice']
        Stock(stock_id = stockID, name = item_name, category = category, quantity=quantity, vendors=vendors,
        sale_price=sale_price, cost_price=cost_price).save()
        msg = 'Item inserted Successfully'
        return render(request, "insertItem.html", {'msg':msg})
    else:
        msg = 'Item was not inserted successfully'
        return render(request, "insertItem.html", {'msg':msg})

def editItem(request):
    if request.method == 'POST':
        stockID = request.POST['stock_id']
        item_name = request.POST['stock_name']
        category = request.POST['stock_category']
        quantity = request.POST['stock_quantity']
        vendors = request.POST['stock_vendors']
        sale_price = request.POST['stock_sale_price']
        cost_price = request.POST['stock_cost_price']
        Stock.objects.filter(stock_id = stockID).update(name=item_name, category=category,quantity=quantity,vendors=vendors,
        sale_price=sale_price, cost_price=cost_price)
        return HttpResponseRedirect("inventory")
    else:
        return HttpResponse("Not Found")

def post_list(request):
    all_post = Stock.objects.all().order_by('id')
    pagenitor = Paginator(all_post, 3)
    page_number = request.GET.get('page')
    data = pagenitor.get_page(page_number)
    return render(request, 'home.html', {'data':data})

def oldProductList(request):
    id = request.GET['id']
    request.session['invoice_id'] = id
    invoice_obj  = Sale.objects.get(invoice_id = id)
    my_list = []
    products = json.loads(invoice_obj.products)
    for data in products:
        my_dict = {}
        my_dict['name'] = data['name']
        my_dict['code'] = str(data['code'])
        my_dict['sale_price'] = str(data['sale_price'])
        my_dict['quantity'] = str(data['quantity'])
        my_list.append(my_dict)
    
    return HttpResponse(json.dumps(my_list))

def return_items(request):
    name = request.GET['name']
    invoice_id = request.GET['id']
    quantity = request.GET['quantity']
    print(quantity)
    sale_obj = Sale.objects.get(invoice_id = invoice_id)
    products = json.loads(sale_obj.products)
    return_price = 0
    new_list = []
    for data in products:
        if data['name'] == name:
            my_dict = {}
            new_quantity = int(data['quantity']) - int(quantity)
            data['quantity'] = new_quantity

            my_dict['name'] = name
            my_dict['quantity'] = quantity
            my_dict['sale_price'] = data['sale_price']
            found = False
            try:
                previous_returns = request.session['returns']
                for data in previous_returns:
                    if data['name'] == name:
                        data['quantity'] = int(data['quantity']) + int(quantity)
                        request.session['returns'] = previous_returns
                        found = True
                        break
                if found == False: 
                    previous_returns.append(my_dict)
                    request.session['returns'] = previous_returns
            except:
                new_list.append(my_dict)
                request.session['returns'] = new_list
    print(products)
    json_data = json.dumps(products)
    Sale.objects.filter(invoice_id = invoice_id).update(products = json_data)
    #         return_price = float(data['sale_price']) * 1
    my_list = []
    my_list.append(name)
    return HttpResponse(json.dumps(my_list))





def return_bill(request):
    previous_returns = request.session['returns']
    return_amount = 0
    stock_list = Stock.objects.all()
    for data in previous_returns:
        syock_obj = stock_list.get(name = data['name'])
        new_quantity = syock_obj.quantity + int(data['quantity'])
        Stock.objects.filter(name = data['name']).update(quantity = new_quantity)
        
        return_amount += int(data['quantity']) * float(data['sale_price'])
    data = {"previous_returns":previous_returns, 'return_amount':return_amount}
    json_data = json.dumps(previous_returns)
    sale_obj = Sale.objects.get(invoice_id = request.session['invoice_id'])
    Return(return_list = json_data, invoice_id = sale_obj, amount = return_amount).save()
    del request.session['invoice_id']
    del request.session['returns']

    template=get_template("pdfReturnbill.html")
    data_p=template.render(data)
    response=BytesIO()

    pdfPage=pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")),response, link_callback=link_callback)
    if not pdfPage.err:
        return HttpResponse(response.getvalue(),content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename=Client_Summary.pdf'
        return response
    else:
        return HttpResponse("Error Generating PDF")


def orderList(request):
    sale_objs = Sale.objects.all()
    return render(request,'orderList.html',{'sale_objs':sale_objs})
    




def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
                if not isinstance(result, (list, tuple)):
                        result = [result]
                result = list(os.path.realpath(path) for path in result)
                path=result[0]
        else:
                sUrl = settings.STATIC_URL        # Typically /static/
                sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                mUrl = settings.MEDIA_URL         # Typically /media/
                mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                if uri.startswith(mUrl):
                        path = os.path.join(mRoot, uri.replace(mUrl, ""))
                elif uri.startswith(sUrl):
                        path = os.path.join(sRoot, uri.replace(sUrl, ""))
                else:
                        return uri

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path


def create_bill_pdf(request):
    currentYear = datetime.now().year
    currentMonth = datetime.now().month
    discount = request.session['discount']
    order = request.session['purchases']
    print(discount)
    print(type(discount))
    # print(f'orders : {order}')
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
    lst = my_list

    after_discount = total - (total * int(discount) / 100)
    json_data = json.dumps(my_list)
    Sale(total = after_discount, products = json_data,month = currentMonth,year =currentYear, sub_total=total , discount=discount,).save()
    stock = Stock.objects.all()
    for data in order:
        stock_obj = stock.get(name = data['name'])
        new_quantity = stock_obj.quantity - int(data['quantity'])
        Stock.objects.filter(name = data['name']).update(quantity = new_quantity)

    print(f'order : {order}')
    data = {"purchases":lst,'total':after_discount,'discount':discount,'total_price':total}
    del request.session['discount']
    del request.session['purchases']

    template=get_template("pdfCreatebill.html")
    data_p=template.render(data)
    response=BytesIO()
 

    pdfPage=pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")),response, link_callback=link_callback, options= { 'page-height': '250mm', 'page-width': '210mm' } )
    if not pdfPage.err:
        return HttpResponse(response.getvalue(),content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename=Client_Summary.pdf'
        return response
    else:
        return HttpResponse("Error Generating PDF")


from datetime import datetime
from django.db.models import Sum

def adminHome(request):
    currentYear = datetime.now().year
    currentMonth = datetime.now().month

    labels = []
    total_sales = []
    total = 0

    totalSales = Sale.objects.aggregate(Sum('total'))['total__sum']

    totalquantity = Stock.objects.aggregate(Sum('quantity'))['quantity__sum']

    month_list = ['January','February','March','April','May','June','July','august','September','October','November','December']

    counter =  0
    month = 0
    for data in month_list:
      
        sale_obj = Sale.objects.filter(year=currentYear)
        for data in range(1, 13):
            month_sale = sale_obj.filter(month = data)
            for sale in month_sale:
                total +=float(sale.total)
            total_sales.append(total)  
            total = 0  

        # print(f'total_sales {total_sales}')
        labels.append(month_list[counter])
        counter = counter + 1
        month = month + 1


    return render(request,'adminHome.html',{'totalSales':totalSales,'totalquantity':totalquantity,'data':total_sales,'labels' :labels})

def RegisterVendorPage(request):
    return render(request,'vendorRegister.html')



def register_vendour(request):
    name = request.POST['name']
    contact = request.POST['contact']
    address = request.POST['address']
    company = request.POST['company']
    Vendor(name=name, contact=contact, address=address, company=company).save()
    return redirect(RegisterVendorPage)


def view_vendors(request):
    vendors = Vendor.objects.all()
    return render(request, 'viewVendor.html', {'vendors':vendors})




def edit_vendour_page(request):
    id = request.GET['id']
    obj = Vendor.objects.get(vendor_id = id)
    return render(request, 'editVendorPage.html', {'obj':obj, 'id':id})


def edited_vendors(request):
    id = request.POST['id']
    name = request.POST['name']
    contact = request.POST['contact']
    address = request.POST['address']
    company = request.POST['company']
    Vendor.objects.filter(vendor_id = id).update(name=name, contact=contact, address=address, company=company)
    return redirect(view_vendors)


def delete_vendor(request):
    id = request.GET['id']
    Vendor.objects.filter(vendour_id = id).delete()
    return redirect(view_vendors)


def returnList(request):
    return_obj = Return.objects.all()

    return render(request,'returnList.html',{'return_obj':return_obj})


def returnDetails(request):
    id = request.GET['id']
    return_obj = Return.objects.get(return_id = id)
    products= json.loads(return_obj.return_list)
    my_list =[]

    for data in products:
        my_dict ={}
        my_dict['name'] = data['name']
        my_dict['quantity'] = data['quantity']
        my_dict['price'] = data['sale_price']
        my_dict['total'] = return_obj.amount
      
        
        my_list.append(my_dict)

    return HttpResponse(json.dumps(my_list))


def saleDetails(request):
    id = request.GET['id']
    print(f'id :{id}')
    sale_obj = Sale.objects.get(invoice_id = id)
    products= json.loads(sale_obj.products)
    my_list =[]

    for data in products:
        my_dict ={}
        my_dict['name'] = data['name']
        my_dict['quantity'] = data['quantity']
        my_dict['price'] = data['sale_price']
        my_dict['total'] = str(sale_obj.total)
        my_list.append(my_dict)

    return HttpResponse(json.dumps(my_list))

    

def view_order_summary(request):
    month = request.POST['month']
    mon = int(month)
    # print(mon)
    myMonth = calendar.month_name[mon]
    print(f'myMonth : {myMonth}')
    # print(f'month :{month}')
    year = request.POST['year']
    print(f'year :{year}')
    sales = Sale.objects.filter(month = month, year = year)
    return render(request,'orderList.html ',{'sales':sales ,'myMonth':myMonth,'year':year })

def view_allReturns_summary(request):
    month = request.POST['month']
    mon = int(month)
    print(mon)
    myMonth = calendar.month_name[mon]
    print(myMonth)
    print(f'month :{month}')
    year = request.POST['year']
    print(f'year :{year}')
    sales = Return.objects.filter(month = month, year = year)
    return render(request,'returnList.html ',{'sales':sales ,'myMonth':myMonth,'year':year })


    