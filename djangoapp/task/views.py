from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Game, Buyer

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
    buyer = None
    if 'buyer_name' in request.session:
        buyer = Buyer.objects.get(name=request.session['buyer_name'])

    context = {
        'title': 'Платформа',
        'text': 'Раздел с платформами.',
        'main_menu': get_main_menu(),
        'platform_menu': ['главная', 'магазин', 'корзина'],
        'buyer': buyer,
    }
    return render(request, 'task/platform.html', context)
def games(request):
    games_list = Game.objects.all()
    context = {
        'title': 'Игры',
        'text': 'Список доступных игр',
        'main_menu': get_main_menu(),
        'games': games_list,
    }
    return render(request, 'task/games.html', context)
def cart(request):
    title = 'Корзина'
    cart_items = request.session.get('cart', {})
    buyer = None
    if 'buyer_name' in request.session:
        buyer_name = request.session['buyer_name']
        buyer = Buyer.objects.get(name=buyer_name)
    context = {
        'title': title,
        'main_menu': get_main_menu(),
        'cart_items': cart_items,
        'buyer': buyer,
    }
    return render(request, 'task/cart.html', context)
def add_to_cart(request, game_name):
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
    if game_name in cart:
        cart[game_name] += 1
    else:
        cart[game_name] = 1
    request.session['cart'] = cart
    return redirect('games')
def clear_cart(request):
    request.session['cart'] = {}
    return JsonResponse({'status': 'ok'})

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = int(request.POST.get('age'))
        balance = float(request.POST.get('balance'))

        # Проверка: существует ли уже покупатель с таким именем
        if not Buyer.objects.filter(name=name).exists():
            buyer = Buyer.objects.create(name=name, balance=balance, age=age)
            request.session['buyer_name'] = buyer.name
            return redirect('profile', username=buyer.name)
        else:
            return render(request, 'task/register.html', {
                'error': 'Пользователь с таким именем уже существует!',
                'main_menu': get_main_menu(),
            })

    return render(request, 'task/register.html', {'main_menu': get_main_menu()})

def profile(request, username):
    if 'buyer_name' not in request.session:
        return redirect('home')  # Если сессия пустая, перенаправляем на главную
    buyer_name = request.session['buyer_name']
    buyer = Buyer.objects.get(name=buyer_name)

    cart_items = request.session.get('cart', [])
    return render(request, 'task/profile.html', {
        'buyer': buyer,
        'cart_items': cart_items,
        'main_menu': get_main_menu(),
    })

def registration(request):
    if request.method == 'POST':
        # Получаем данные
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        age = request.POST.get('age')
        balance = request.POST.get('balance')
        subscribe = request.POST.get('subscribe') == 'on'

        # Проверяем есть ли уже пользователь
        if not Buyer.objects.filter(name=name).exists():
            buyer = Buyer.objects.create(
                name=name,
                age=int(age) if age else 18,
                email=email,
                balance=float(balance) if balance else 0.0,
                message=message,
                subscribe=subscribe,
            )
        request.session['buyer_name'] = buyer.name
        return redirect('profile', username=buyer.name)
    else:
        # Http ответ пользователя:
        return HttpResponse("Пользователь с таким именем уже существует!")

        # Если это GET
    return render(request, 'task/main.html', {'main_menu': get_main_menu()})
from django.http import JsonResponse
def update_cart_quantity(request):
    game_name = request.POST.get('game_name')
    action = request.POST.get('action')

    cart = request.session.get('cart', {})

    if action == 'increase':
        cart[game_name] = cart.get(game_name, 0) + 1
    elif action == 'decrease':
        if game_name in cart:
            cart[game_name] -= 1
            if cart[game_name] <= 0:
                del cart[game_name]

    request.session['cart'] = cart
    return JsonResponse({'status': 'ok'})