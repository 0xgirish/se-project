from django.contrib import admin
from django.urls import path, include

from .views import home_page, contact_page, temp_page, register_view

app_name = "home"

urlpatterns = [
    path('', home_page),
    path('register', register_view),
    path('contact', contact_page),
    path('temp', temp_page),
]
