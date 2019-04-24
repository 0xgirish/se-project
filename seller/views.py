from django.shortcuts import render
from django.http import HttpResponseNotFound

# Create your views here.


def seller_page(request):
    # TODO: add seller dashboard here
    return HttpResponseNotFound(f"TODO: add seller dashboard here, seller/")


def shop_register(request):
    # TODO: define form to register shop
    return HttpResponseNotFound("TODO: define seller/shop_register")


def item_register(request):
    # TODO: define form to register item
    return HttpResponseNotFound("TODO: define seller/item_register")