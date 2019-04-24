from django.contrib.auth.models import User
from barcodelookup.models import Product
from seller.models import UserProfile, ShopProfile, ShopItem

import random

fn = random.randint

NOT_FOUND = "/media/images/product-image-not-found.gif"

base_barcode = 8901234567890
product_name = "Product - {}"


def progress_bar(x, n):
    if n > 10:
        bar = "[" + "=" * x + ">" + " " * (n - x) + "]"
    else:
        bar = "[" + "=" * 5*x + ">" + " " * 5*(n - x) + "]"
    print(bar, end="\r")


print("Creating dummy products...")
progress_bar(0, 25)
# create dummy products
for i in range(25):
    barcode = str(base_barcode + i)
    title = product_name.format(barcode[-3:])
    product = Product(barcode=barcode, image_url=NOT_FOUND, title=title)
    product.save()

    progress_bar(i+1, 25)

# create dummy user profile
user = User(username="foobar", first_name="Ram", last_name="Krishna", password="12ergh90", email="ram@gmail.com")
user.save()

user = UserProfile(user=user, phone="9825205502", address="Bela Chauk, Rupnagar, 140001")
user.save()

shop_names = ["Apna Groceries", "Green World", "Departmental Shop"]
latitudes = [30.9676117, 30.968094, 30.967967]
longitudes = [76.469922, 76.475734, 76.468513]

print("\nCreating dummy shops...")
progress_bar(0, 3)
# create dummy shops
for i in range(3):
    shop = ShopProfile(user=user, latitude=latitudes[i], longitude=longitudes[i], name=shop_names[i])
    shop.save()

    progress_bar(i+1, 3)

products = Product.objects.all()
shops = ShopProfile.objects.all()

description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."

print("\nCreating dummy shop items...")
progress_bar(0, 30)
# create dummy items
for i in range(30):
    product = products[fn(0, 24)]
    shop = shops[fn(0, 2)]
    price = fn(250, 600)
    quantity = fn(3, 20)

    item = ShopItem(product=product, shop=shop, price=price, description=description, quantity=quantity)
    item.save()

    progress_bar(i+1, 30)
