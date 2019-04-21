from django.urls import path
from .views import lookup_product

urlpatterns = [
    path('', lookup_product)
]
