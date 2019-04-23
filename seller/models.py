from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from barcodelookup.models import Product

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    address = models.CharField(max_length=1000, default='')
    phone = models.CharField(max_length=14, default='')
    website = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.user.username

class ShopProfile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    address = models.TextField(default="")
    website = models.CharField(default="")
    review_stars = models.IntegerField(default=-1)

class ShopItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.PROTECT)
    shop = models.OneToOneField(ShopProfile, on_delete=models.CASCADE)
    price = models.IntegerField(default=-1)
    description = models.TextField(default="")
    image_url = models.TextField(default="")
    quantity = models.IntegerField(default=1)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()
