from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from openstore.settings import SEARCH_THRESHOLD
from seller.forms import RegistrationForm
from seller.models import ShopItem, ShopProfile, UserProfile
from barcodelookup.models import Product

def search_model(model, query, *v):
    # can not be
    vector = SearchVector(*v)
    result = model.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank').filter(rank__gte=SEARCH_THRESHOLD)
    if model == Product:
        print(f"\n\n====================== Product {len(result)}=====================\n\n")
        items = ShopItem.objects.filter(product__in=result)
    elif model == ShopProfile:
        print(f"\n\n====================== Shop {len(result)}=====================\n\n")
        items = ShopItem.objects.filter(shop__in=result)
    elif model == ShopItem:
        print(f"\n\n====================== Item {len(result)}=====================\n\n")
        items = result
    else:
        items = None
    
    return items

def search(request):
    q = request.GET['q']
    query = SearchQuery(q)
    # search using products
    result_items = list()
    result_items.append(search_model(Product, query, 'title', 'description'))
    result_items.append(search_model(ShopProfile, query, 'name', 'website'))
    result_items.append(search_model(ShopItem, query, 'description'))

    result = list()
    for items in result_items:
        if items is None:
            print("\n\n====================== NONE =====================\n\n")
            continue
        for item in items:
            result.append(item)

    return result

def check_q(request):
    try:
        request.GET['q']
        return True
    except:
        return False

# Create your views here.
def home_page(request):
    form = RegistrationForm

    if request.method == "GET" and check_q(request):
        items = search(request)
    else:
        items = ShopItem.objects.all()
    context = {
        "items": items,
        "form": form,
    }
    return render(request=request, template_name="index.html", context=context)


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("/")
        else:
            for msg in form.error_messages:
                print(msg)
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(request=request,
                          template_name="index.html",
                          context={"form": form})
    else:
        return HttpResponseNotFound("404")


def contact_page(request):
    return render(request, "contact.html")

def temp_page(request):
    if request.method == "GET":
        product_id = request.GET["pid"]
        product = Product.objects.get(id=product_id)
        shopItem = ShopItem.objects.filter(product=product)
        args = {'product': product, 'shops': shopItem}
        return render(request, "single.html", args)
    return redirect(request, "/")


def location(request):
    return render(request, "location.html")


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("/")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(request=request,
                          template_name="register.html",
                          context={"form": form})
    form = RegistrationForm
    return render(request = request,
                  template_name = "register.html",
                  context={"form":form})


@login_required
def logout_request(request):
    logout(request)
    return redirect("/")


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="index.html",
                  context={"form": form})

