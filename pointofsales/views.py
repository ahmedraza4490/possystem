from django.shortcuts import render,redirect
from stocks.models import Stock
from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
import calendar
# from datetime import datetime
from stocks.views import adminHome
import datetime
from django.contrib.auth import authenticate



data = {}

def home(request):
    today = date.today()
    ItemsList = Stock.objects.all()
    four_items = ItemsList.order_by('name')[0:4]
    # order_by('your_field')[0:4].get()
    print(f'2 : {four_items}')
    d1 = today.strftime("%B %d, %Y")
    
    now = datetime.datetime.now()
    day = (now.strftime("%A"))
    print('staff home')
    try:
        del request.session['purchases']
        del request.session['discount']
    except:
        print('no purchases yet')

    currentMonth = datetime.datetime.now()
    d2 = currentMonth.strftime("%B %d, %Y")
    # myMonth = calendar.month_name[currentMonth]
    return render(request, 'home.html',{'ItemsList':ItemsList,'four_items':four_items, 'd1':d1,'day':day})


# def getItems(request):
#     print('Test')
#     stockID = request.GET['id']
#     objstock =  Stock.objects.filter(stock_id = stockID)
#     print(objstock)
#     data = {stockID : objstock}
#     print(data)
#     return render(request, 'home.html', {'data': data}) 
    # return render_to_response(request,'home.html',{'data':objstock})


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

        
#         user = 0

#         try:
#             user = authenticate(username = username, password = password)
#         except:
#             user = None
#         if user is not None:
#             if user.is_active:
#                 if user.is_superuser:
#                     # user is faculty
#                     request.session['user'] =  username
#                     return redirect(adminHome)
#                 else:
                   
#                     # if not current_time in range(1,7):
#                     print("hello ")
#                     msg = 'You are not Allowed To Login at this Time'
#                     messages.success(request,msg)
#                     return render(request,'loginPage/loginPage.html')

                   
#                         # print('else enter')
#                         # request.session['user'] =  username
#                         # return redirect(all_users)
#             else:
#                 msg = "User is Not Active Anymore"
#                 return render(request, "loginpages/adminlogin.html", {"msg":msg})
#         else:
#             messages.success(request, 'Username or Password is incorrect')
#             return redirect(login_page)

# def logout(request):
#     del request.session['user']

    
#     auth.logout(request)