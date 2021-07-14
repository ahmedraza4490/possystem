from . import views
from django.urls import path

urlpatterns = [
    path('invoice/', views.invoice, name='invoice'),
]