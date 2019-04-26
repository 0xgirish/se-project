from django.contrib import admin
from django.urls import path, include

from .views import home_page, contact_page, register_view, product_page

app_name = "home"

urlpatterns = [
    path('', home_page),
    path('register', register_view),
    path('contact', contact_page),
    path('product', product_page),
]
