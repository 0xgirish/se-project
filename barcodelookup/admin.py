from django.contrib import admin
from .models import Product, Book, UserProfile
# Register your models here.

# register Product database for admin panel
admin.site.register(Product)
admin.site.register(Book)
admin.site.register(UserProfile)
