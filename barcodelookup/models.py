from django.db import models

# image url with image not found
NOT_FOUND = "/media/images/product-image-not-found.gif"


# Create your models here.
class Product(models.Model):
    """product details for barcode"""

    barcode = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=200, default='Unknown')
    description = models.TextField(default="not available")
    image_url = models.TextField(default=NOT_FOUND)

    def __str__(self):
        return self.title


# TODO: Piyush implement scraping demon for the asin table using postgres database connection
# TODO: Or add the demon as a app in the project, ref. python manage.py startapp demon,   add code to demon folder
class Asin(models.Model):
    """
    Asin table contains information about, product on amazon.in/dp/asin
    checked: should be checked by amazon scraping demon to add information to the database, e.g. price, availability, image_url
    """

    NOT_AVAILABLE = -1

    product = models.OneToOneField(Product, on_delete=models.PROTECT)
    asin = models.CharField(max_length=40)
    image_url = models.TextField(default=NOT_FOUND)
    is_available = models.BooleanField(default=False)
    price = models.IntegerField(default=NOT_AVAILABLE)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.asin

