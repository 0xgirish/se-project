from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required

from .models import ShopProfile, ShopItem, UserProfile
from .forms import ShopRegistrationForm, ItemRegistrationForm

# Create your views here.


def seller_page(request):
    # TODO: add seller dashboard here
    return render(request, "seller/profile.html")


@login_required
def account_access(request):
    print("\n\n---------------------------------------------------------------------\n\n")
    user = UserProfile.objects.get(user=request.user)
    shops = ShopProfile.objects.filter(user=user) 
    shopitem = ShopItem.objects.filter(shop__in=shops)
    # print("\n\n", f"length == {len(shopitem)}", "\n\n")
    args = {'shops': shops, 'userP': user, 'items': shopitem}
    return render(request, 'seller/dashboard.html', args)


def shop_register(request):
    # TODO: define form to register shop
    if request.method == 'POST':
        form = ShopRegistrationForm(request.POST)
        if form.is_valid():
            shop = form.save()
            shop_name = form.cleaned_data.get('name')
            messages.success(request, f"New shop created: {shop_name}")
            return redirect("/seller/profile")
        else:
            error_messages = ""
            for msg in form.error_messages:
                error_messages = msg + "\n"
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(request, "seller/form.html", context={"form": form})
    
    form = ShopRegistrationForm
    submit_url = "/seller/shop/register"
    todo_html = "seller/shop_register.html"
    context = {
        "form": form,
        "submit_url": submit_url,
        "todo_html": todo_html,
    }
    return render(request, "seller/form.html", context)


def item_register(request):
    # TODO: define form to register item
    if request.method == 'POST':
        form = ItemRegistrationForm(request.POST)
        if form.is_valid():
            item = form.save()
            product_id = form.cleaned_data.get('product_id')
            shop_id = form.cleaned_data.get('shop_id')
            messages.success(request, f"New item created for shop {shop_id}: {product_id}")
            return redirect("/seller/profile")
        else:
            error_messages = ""
            for msg in form.error_messages:
                error_messages = msg + "\n"
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(request, "seller/form.html", context={"form": form})
    
    form = ItemRegistrationForm
    submit_url = "/seller/item/register"
    todo_html = "seller/item_register.html"
    context = {
        "form": form,
        "submit_url": submit_url,
        "todo_html": todo_html,
    }
    return render(request, "seller/form.html", context)