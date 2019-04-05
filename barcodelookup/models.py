from django.db import models

# image url with image not found
NOT_FOUND = "https://i.ibb.co/dj1qb0D/product-image-not-found.gif"

# Create your models here.
class Product(models.Model):
    """product details for barcode"""

    barcode = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=200, default='')
    description = models.TextField(default="")

    def __str__(self):
        return self.title


class Book(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    author = models.CharField(max_length=40)
    # cover photo of book
    cover = models.TextField(default=NOT_FOUND)
    no_of_pages = models.IntegerField()
    publisher = models.CharField(max_length=120)
    publish_data = models.CharField(max_length=40)

    def __str__(self):
        return self.product.title
