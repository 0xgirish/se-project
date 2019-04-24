from django.urls import path
from .views import seller_page, shop_register, item_register


urlpatterns = [
    path('profile', seller_page),
    path('shop/register', shop_register),
    path('item/register', item_register),
]
