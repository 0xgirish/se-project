from django.shortcuts import render
from barcodelookup.models import Product

# Create your views here.
def home_page(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, "home.html", context)

def location(request):
	return render(request, "location.html")
