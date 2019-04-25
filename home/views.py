from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from seller.forms import RegistrationForm
from django.contrib.auth.decorators import login_required

from seller.models import ShopItem, ShopProfile, UserProfile


# Create your views here.
def home_page(request):
    items = ShopItem.objects.all()
    form = RegistrationForm
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
    return render(request, "single.html")


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


@login_required
def account_access(request):
    user_prof = UserProfile.objects.filter(user=request.user)
    args = {'user': request.user, 'shops': ShopProfile.objects.filter(user__in=user_prof), 'userP': user_prof}
    return render(request, 'account.html', args)
