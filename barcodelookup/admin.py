from django.contrib import admin
from .models import Product, Book
# Register your models here.

# register Product database for admin panel
admin.site.register(Product)
admin.site.register(Book)