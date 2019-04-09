from django.shortcuts import render
from barcodelookup.models import Product
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def home_page(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, "home.html", context)

def location(request):
	return render(request, "location.html")

def register(request):
	form = UserCreationForm
	return render(request = request, template_name = "register.html", context={"form":form})
