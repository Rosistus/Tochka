from django.shortcuts import render, redirect
from django.http import HttpResponse

import main.forms
from users.models import User
from main.models import BlessLimit
from main.forms import BlessLimitForm
from django.urls import reverse


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
    form = BlessLimitForm()
    context = {
        "title": 'Embrace God',
        'username': request.user.username,
        'blessed_users': blessed_users,
        'is_blessed': is_blessed,
        'bless_counter': bless_counter(),
        'form': form,
    }

    return render(request, 'main/index.html', context)


def about(request):
    context = {
        "title": 'Об авторе',
    }
    return render(request, 'main/about.html', context)


def change_limit(request):
    user = request.user
    form = BlessLimitForm(data=request.POST)
    new_limit = int(request.POST['limit'])
    current_limit = BlessLimit.objects.first()
    blessed_users = User.objects.filter(blessed=True).count()
    if form.is_valid():
        if user.is_staff and request.method == 'POST':
            if new_limit >= blessed_users:
                current_limit.value = new_limit
                current_limit.save()
    return redirect(reverse('main:index'))




