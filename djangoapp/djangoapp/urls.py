"""
URL configuration for djangoapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from task.views import home
from task.views import platform
from task.views import games
from task.views import cart
from task.views import add_to_cart
from task.views import clear_cart
# from task.views import register
from task.views import profile
from task.views import registration
from task.views import update_cart_quantity



urlpatterns = [
    path('admin/', admin.site.urls),
    path('platform/', platform, name='platform'),
    path('games/', games, name='games'),
    path('cart/', cart, name='cart'),
    path('', home, name='home'),
    path('add/<str:game_name>/', add_to_cart, name='add_to_cart'),
    path('clear-cart/', clear_cart, name='clear_cart'),
    # path('register/', register, name='register'),
    path('profile/<str:username>/', profile, name='profile'),
    path('registration/', registration, name='registration'),
    path('update-cart/', update_cart_quantity, name='update_cart_quantity'),

]
