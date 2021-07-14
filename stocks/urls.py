from django.urls import path
from . import views

urlpatterns = [
   path('inventory',views.inventory),
   path('insertitem',views.insertItem),
   path('insert',views.insertData),
   path('delete',views.deleteItem),
   path('edit',views.editItem),
   path('update',views.editItem),
   # path('make_bill',views.make_bill),


   path('returnProduct',views.returnProduct),
   path('oldProductList',views.oldProductList),
   path('return_items',views.return_items),
   path('return_bill',views.return_bill, name="return_bill"),
   path('create_bill_pdf',views.create_bill_pdf, name="create_bill_pdf"),





   path('adminHome',views.adminHome, name="adminHome"),
   path('RegisterVendorPage',views.RegisterVendorPage, name="RegisterVendorPage"),
   path('register_vendour',views.register_vendour, name="register_vendour"),


   path('view_vendors',views.view_vendors, name="view_vendors"),

   path('edit_vendour_page', views.edit_vendour_page, name='edit_vendour_page'),

   path('edited_vendors', views.edited_vendors, name='edited_vendors'),

   path('delete_vendor', views.delete_vendor, name='delete_vendor'),

   path('orderList', views.orderList, name='orderList'),

   path('returnList', views.returnList, name='returnList'),
   path('returnDetails', views.returnDetails, name='returnDetails'),

   path('view_order_summary', views.view_order_summary, name='view_order_summary'),

   path('saleDetails', views.saleDetails, name='saleDetails'),

   path('view_allReturns_summary', views.view_allReturns_summary, name='view_allReturns_summary'),

   

   

   

   



   
   
   

   
   
   
]
