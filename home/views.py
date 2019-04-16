from django.shortcuts import render, redirect
from barcodelookup.models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def home_page(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, "home.html", context)


def location(request):
	return render(request, "location.html")

def register(request):
	if request.method=='POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect("/")
		else:
			for msg in form.error_messages:
				print(form.error_messages[msg])
			return render(request = request,
                          template_name = "register.html",
                          context={"form":form})
	form = UserCreationForm
	return render(request = request,
                  template_name = "register.html",
                  context={"form":form})
