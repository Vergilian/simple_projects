from django.shortcuts import render, redirect

# Create your views here.
def get_main_menu():
    return [
        {'title': 'Платформа', 'url_name': 'platform'},
        {'title': 'Игры', 'url_name': 'games'},
        {'title': 'Корзина', 'url_name': 'cart'},
    ]
def home(request):
    context = {
        'title': 'Главная страница',
        'text': 'Добро пожаловать на сайт!',
        'main_menu': get_main_menu(),
    }
    return render(request, 'task/main.html', context)

def platform(request):
    context = {
        'title': 'Платформа',
        'text': 'Раздел с платформами.',
        'main_menu': get_main_menu(),
        'platform_menu': ['главная', 'магазин', 'корзина'],
    }
    return render(request, 'task/platform.html', context)
def games(request):
    context = {
        'title': 'Игры',
        'text': 'Список доступных игр',
        'main_menu': get_main_menu(),
        'games': ['Beholder', 'Beholder 2', 'Beholder 3'],
    }
    return render(request, 'task/games.html', context)
def cart(request):
    title = 'Корзина'
    cart_items = request.session.get('cart', [])
    context = {
        'title': title,
        'main_menu': get_main_menu(),
        'cart_items': cart_items,
    }
    return render(request, 'task/cart.html', context)
def add_to_cart(request, game_name):
    cart = request.session.get('cart', [])
    if game_name not in cart:
        cart.append(game_name)
    request.session['cart'] = cart
    return redirect('games')
def clear_cart(request):
    request.session['cart'] = []
    return redirect('cart')
