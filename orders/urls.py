from orders import views
from django.urls import path

urlpatterns = [
    path('getItems/', views.getItems, name='getItems'),
    path('getItemByName', views.getItemByName, name='getItemByName'), 
    path('deleItem/', views.deleteItem, name='deleteItem'),
    path('add_item', views.add_item, name='add_item'),
    path('subtract_item', views.subtract_item, name='subtract_item'),
    path('delete_item', views.delete_item, name='delete_item'),
    path('create_order', views.create_order, name='create_order'),

    
    path('add_ten_items', views.add_ten_items, name='add_ten_items'),
    path('increase_quantity', views.increase_quantity, name='increase_quantity'),
    path('save_discount', views.save_discount, name='save_discount'),

    
]