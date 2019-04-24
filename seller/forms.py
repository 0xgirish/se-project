from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ShopProfile, ShopItem
from barcodelookup.models import Product


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = {
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class RegisterShopForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    latitude = forms.FloatField(required=True)
    longitude = forms.FloatField(required=True)
    website = forms.FloatField()

    class Meta:
        model = ShopProfile
        fields = {
            'user',
            'name',
            'latitude',
            'longitude',
            'website',
            'review_stars',
        }

    def save(self, commit=True):
        shop = super(RegisterShopForm, self).svae(commit=False)
        shop.name = self.cleaned_data['name']
        shop.latitude = self.cleaned_data['latitude']
        shop.longitude = self.cleaned_data['longitude']
        shop.website = self.cleaned_data['website']

        if commit:
            shop.save()
        return shop


class RegisterItemForm(forms.Form):
    image_url = forms.ImageField(allow_empty_file=True)

    class Meta:
        model = ShopItem
        fields = {
            'shop',
            'barcode',
            'price',
            'priority',
            'image_url',
            'description',
            'quantity',
        }

    def save(self, commit=True):
        item = super(RegisterItemForm, self).svae(commit=False)
        item.price = self.cleaned_data['price']
        item.priority = self.cleaned_data['priority']
        item.quantity = self.cleaned_data['quantity']
        item.description = self.cleaned_data['description']

        barcode = self.cleaned_data['barcode']
        shop_id = self.cleaned_data['shop']
        product = Product.objects.get(barcode=barcode)
        shop = ShopProfile.objects.get(id=shop_id)

        item.product = product
        item.shop = shop

        if commit:
            item.save()
        return item
