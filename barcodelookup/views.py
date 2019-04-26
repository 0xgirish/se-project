from django.http import HttpResponse
from django.core import serializers
from .models import Product, Asin

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
        return product
    except Product.DoesNotExist:
        return None


def get_names(resp):
    size = len(resp)
    names = ""
    for i in range(size):
        if i == size-1:
            names += resp[i]["name"]
        else:
            names += resp[i]["name"] + ", "
    return names

def google_custom_search(barcode):
    api_url = GOOGLE_API.format("AIzaSyBe6b_gfR1E8-2pOQb3HWUYISBzt1-esg8", "005395856063250790473:if-ztsdoo8m", barcode)
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


def lookup_product(request, barcode):
    # add author 
    
    product = lookup_in_database(barcode)
    if product != None:
        s_product = serializers.serialize('json', [product, ])
        json_data = json.loads(s_product)
        field = json_data[0]
        fields = json_data[0]['fields']
        pk = field['pk']
        fields['pk'] = 269
        print(type(fields))
        return HttpResponse([fields])

    # check if barcode is isbn
    if is_isbn(barcode):
        api_url = ISBN_API_URL.format(barcode)
        resp = requests.get(api_url)
        r = json.loads(resp.text)
        if len(r) != 0:
            item = r["ISBN:{}".format(barcode)]
            image_url = item["cover"]["medium"]
            title = item["title"]
            description = "Authors: {}\nPublishers: {}".format(get_names(item["authors"]), get_names(item["publishers"]))
            product = Product(barcode=barcode, title=title, image_url=image_url, description=description)
            product.save()
            s_product = serializers.serialize('json', [product, ])
            json_data = json.loads(s_product)
            fields = json_data[0]["fields"]
            return HttpResponse([fields])
    result = google_custom_search(barcode)
    if result is None:
        return HttpResponse(json.dumps({"result": 0}))
    # TODO: add context_link if amazon,  ASIN
    title, image_url, context_link = result[0], result[1], result[2]
    product = Product(barcode=barcode, title=title, image_url=image_url)
    product.save()
    s_product = serializers.serialize('json', [product, ])
    if context_link.find("amazon") != -1:
        link = "/".join(context_link.split("/")[3:])
        link = "https://www.amazon.in/" + link
        asin_code = context_link.split("/")[-1]
        asin = Asin(product=product, asin=asin_code, image_url=link)
        asin.save()
    json_data = json.loads(s_product)
    field = json_data[0]
    fields = json_data[0]['fields']
    pk = field['pk']
    fields['pk'] = 269
    return HttpResponse([fields])