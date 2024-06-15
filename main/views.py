from django.shortcuts import render
from django.http import HttpResponse
from users.models import User
from main.models import BlessLimit


def bless_counter():
    limit = BlessLimit.objects.first()
    max_blessed = limit.value
    blessed_users = User.objects.filter(blessed=True)
    bless_count = max_blessed - blessed_users.count()
    return bless_count


def index(request):
    blessed_users = User.objects.filter(blessed=True)
    if request.user.is_authenticated:
        is_blessed = request.user.blessed
    else:
        is_blessed = 0
    context = {
        "title": 'Embrace God',
        'username': request.user.username,
        'blessed_users': blessed_users,
        'is_blessed': is_blessed,
        'bless_counter':     bless_counter()
    }

    return render(request, 'main/index.html', context)


def about(request):
    context = {
        "title": 'Об авторе',
    }
    return render(request, 'main/about.html', context)

