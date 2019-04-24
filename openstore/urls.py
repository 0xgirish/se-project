"""openstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, register_converter
from django.conf import settings
from django.conf.urls.static import static
from home.views import register
from home.views import logout_request
from home.views import login_request
from home.views import account_access

from barcodelookup import converter

app_name = "openstore"

register_converter(converter.BarcodeConverter, 'ean')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('lookup/<ean:barcode>', include('barcodelookup.urls')),
    path('', include('home.urls')),
    path("register", register, name="register"),
    path("logout", logout_request, name="logout"),
    path("login", login_request, name="login"),
    path("account", account_access, name="account"),
    path('seller/', include('seller.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
