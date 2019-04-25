from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ShopProfile, ShopItem, UserProfile
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



class ShopRegistrationForm(forms.ModelForm):
    user_id = forms.IntegerField(required=True)

    class Meta:
        model = ShopProfile
        fields = [
            "name",
            "latitude",
            "longitude",
            "website",
        ]

    def save(self, commit=True):
        shop = super(ShopRegistrationForm, self).save(commit=False)
        user_id = self.cleaned_data['user_id']
        shop.user = UserProfile.objects.get(user=user_id)
        shop.name = self.cleaned_data['name']
        shop.latitude = self.cleaned_data['latitude']
        shop.longitude = self.cleaned_data['longitude']
        shop.website = self.cleaned_data['website']

        if commit:
            shop.save()
        return shop

class ItemRegistrationForm(forms.ModelForm):
    shop_id = forms.IntegerField(required=True)
    product_id = forms.IntegerField(required=True)

    class Meta:
        model = ShopItem
        fields = [
            "price",
            "priority",
            "description",
            "image_url",
            "quantity",
        ]

    def save(self, commit=True):
        item = super(ItemRegistrationForm, self).save(commit=False)
        product_id = self.cleaned_data['product_id']
        shop_id = self.cleaned_data['shop_id']
        item.product = Product.objects.get(id=product_id)
        item.shop = ShopProfile(id=shop_id)
        item.price = self.cleaned_data['price']
        item.quantity = self.cleaned_data['quantity']
        item.priority = self.cleaned_data['priority']
        item.image_url = self.cleaned_data['image_url']
        item.description = self.cleaned_data['description']

        if commit:
            item.save()

        return item

