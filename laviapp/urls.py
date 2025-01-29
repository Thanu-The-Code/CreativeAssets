from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import home



urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('shop/', views.shop, name='shop'),
    path('contact/', views.contact, name='contact'),
    path('home/', home, name='home'),
 
    path('send_contact_email/', views.send_contact_email, name='send_contact_email'),
    path('contact/send_contact_email/', views.send_contact_email, name='send_contact_email'),

    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('more-items/', views.more_items, name='more_items'),  # Show all items
    path('more-items/<str:category>/', views.filtered_items, name='filtered_items'),  # Show items filtered by category
    path('item-details/<int:item_id>/', views.item_details, name='item_details'),
    path('buy-now/<int:item_id>/', views.buy_now, name='buy_now'),

    path('create-razorpay-order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('razorpay-success/', views.razorpay_success, name='razorpay_success'),
    
    path('success/', views.success, name='success'),
    path('my_orders/', views.my_orders, name='my_orders'),



]




    
  




