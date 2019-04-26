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
            "address",
            "latitude",
            "longitude",
            "website",
        ]

    def save(self, commit=True):
        shop = super(ShopRegistrationForm, self).save(commit=False)
        user_id = self.cleaned_data['user_id']
        shop.user = UserProfile.objects.get(user=user_id)
        shop.address = self.cleaned_data['address']
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
    barcode = forms.IntegerField(required=True)
    image_u = forms.ImageField()
    imagr_ = forms.CharField(max_length=100)

    class Meta:
        model = ShopItem
        fields = [
            "title",
            "price",
            "description",
            "quantity",
        ]

    def save(self, commit=True):
        print(f"\n\n{self.cleaned_data['shop_id']}\n{self.cleaned_data['product_id']}\n\n")
        # item = super(ItemRegistrationForm, self).save(commit=False)
        product_id = self.cleaned_data['product_id']
        shop_id = self.cleaned_data['shop_id']
        product = Product.objects.get(id=product_id)
        shop = ShopProfile(id=shop_id)
        title = str(self.cleaned_data['title'])
        price = int(self.cleaned_data['price'])
        quantity = int(self.cleaned_data['quantity'])
        description = self.cleaned_data['description']

        item = ShopItem(product=product, shop=shop, title=title, price=price, description=description, quantity=quantity)

        if commit:
            item.save()

        return item

