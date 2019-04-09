from django.db import models

# image url with image not found
NOT_FOUND = "https://i.ibb.co/dj1qb0D/product-image-not-found.gif"

# Create your models here.
class Product(models.Model):
    """product details for barcode"""

    barcode = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=200, default='')
    description = models.TextField(default="")
    image_url = models.TextField(default=NOT_FOUND)

    def __str__(self):
        return self.title


class Asin(models.Model):
    product = models.OneToOneField(Product, on_delete=models.PROTECT)
    asin = models.CharField(max_length=40)
    link = models.TextField()

    def __str__(self):
        return self.link

