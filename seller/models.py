from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from barcodelookup.models import Product


NOT_FOUND = "https://i.ibb.co/dj1qb0D/product-image-not-found.gif"


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=1000, default='')
    phone = models.CharField(max_length=14, default='')
    website = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.user.username


# latitude longitude
class ShopProfile(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="")
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    website = models.CharField(default="not available", max_length=100)
    review_stars = models.IntegerField(default=-1)

    def __str__(self):
        return self.name


class ShopItem(models.Model):
    HIGH = 'h'
    MEDIUM = 'm'
    LOW = 'l'

    ITEM_PRIORITY_CHOICES = (
        (HIGH, 'high'),
        (MEDIUM, 'medium'),
        (LOW, 'low'),
    )

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE)
    price = models.IntegerField(default=-1)
    priority = models.CharField(max_length=2, choices=ITEM_PRIORITY_CHOICES, default=MEDIUM)
    description = models.TextField(default="not available")
    image_url = models.TextField(default=NOT_FOUND)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.title


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
