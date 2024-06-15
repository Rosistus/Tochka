from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail
from django.utils import timezone

import main.views
from users.forms import UserLoginForm, UserRegistrationForm
from users.models import User, TempBan


# Create your views here.


def login(request):
    if request.method == 'POST':
        ip = get_user_ip(request)
        obj, created = TempBan.objects.get_or_create(
            defaults={
                'ip_address': ip,
                'time_unblock': timezone.now()
            },
            ip_address=ip
        )

        if obj.time_unblock > timezone.now():
            #if obj.attempts >= 3:
            return render(request, 'auth/Ban.html')
        else:
            form = UserLoginForm(data=request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = auth.authenticate(username=username, password=password)
                obj.delete()
                if user:
                    auth.login(request, user)
                    return HttpResponseRedirect(reverse('main:index'))
            else:
                obj.attempts += 1
                if obj.attempts == 3:
                    obj.time_unblock = timezone.now() + timezone.timedelta(minutes=1)
                obj.save()
    else:
        form = UserLoginForm()

    context = {
        "title": 'Вход',
        'form': form
    }
    return render(request, 'auth/LoginPage.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()
    context = {
        "title": 'Регистрация',
        'form': form,
    }
    return render(request, 'auth/RegisterPage.html', context)


def ban(request):
    context = {
        "title": 'Срамота...',
    }
    return render(request, 'auth/Ban.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))


def bless(request):
    user = request.user
    if (main.views.bless_counter()) > 0 or (main.views.bless_counter() == 0 and user.blessed is True):
        if user.blessed:
            message = '{}, Вы исключены из рая...'.format(request.user.username)
        else:
            message = '{}, Вы успешно попадаете в рай!!!'.format(request.user.username)
        user.blessed = not user.blessed
        user.save()
        if request.user.email is not None:
            try:
                send_mail('New message from Jesus',
                          message,
                          'Jesuswannatalktoyou@yandex.ru',
                          [request.user.email], fail_silently=False)
            except Exception:
                pass

    return redirect(reverse('main:index'))


def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

