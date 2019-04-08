from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .models import Product, Book

import json
import requests
# Create your views here.

ISBN_API_URL = "https://openlibrary.org/api/books?bibkeys=ISBN:{}&format=json&jscmd=data"
GOOGLE_API = "https://www.googleapis.com/customsearch/v1?key={}&cx={}&q={}&searchType=image&fileType=jpg&imgSize=medium&alt=json"

def is_isbn(barcode):
    if str(barcode).startswith("978"):
        return True
    return False

def lookup_in_database(barcode):
    try:
        product = Product.objects.get(barcode=barcode)
    except Product.DoesNotExist:
        return None, None

    if product.is_book:
        book = Book.objects.get(product=product)
        return product, book
    return product, None


def add_product_to_database(json_resp):
    pass

def lookup_product(request, barcode):
    # example test
    # TODO: change function to scrap or do api calls for barcode lookup
    # TODO: 1. Look into openstore database
    # TODO: 2. If not, then look up in https://barcodelookup.com etc
    # books api: https://openlibrary.org/api/books?bibkeys=ISBN:9789352135219&format=json&jscmd=data
    
    product, book = lookup_in_database(barcode)
    if product != None:
        s_product = serializers.serialize('json', [product, ])
        if book == None:
            return HttpResponse(s_product)
        
        s_object = serializers.serialize('json', [product, book, ])
        return HttpResponse(s_object)

    # check if barcode is isbn
    if is_isbn(barcode):
        api_url = ISBN_API_URL.format(barcode)
        resp = requests.get(api_url)
        return HttpResponse(resp)
    else:
        result = google_custom_search(barcode)
        if result is None:
            return HttpResponse(json.dumps({"result": 0}))
        # TODO: add context_link if amazon,  ASIN
        title, image_url, context_link = result[0], result[1], result[2]
        product = Product(barcode=barcode, title=title, image_url=image_url)
        product.save()
        s_product = serializers.serialize('json', [product, ])
        return HttpResponse(s_product)

def google_custom_search(barcode):
    api_url = GOOGLE_API.format("AIzaSyBZVs8cxX4mbesnj-pt55so0DfpSe2PJow", "005395856063250790473:if-ztsdoo8m", barcode)
    resp = requests.get(api_url)
    r = json.loads(resp.text)
    try:
        items = r["items"]
        size = len(items)
        index = 0
        indian = False
        for i in range(size):
            if items[i]["displayLink"].find("amazon.") != -1 and not indian:
                index, indian = i, True
            elif items[i]["displayLink"].find("amazon.in") != -1 and indian:
                index = i
        
        image_url = items[index]["link"]
        context_link = items[index]["image"]["contextLink"]
        title = items[0]["title"]
        return [title, image_url, context_link]
    except KeyError:
        return None