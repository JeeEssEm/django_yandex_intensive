from axes.models import AccessAttempt

from core import utils

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render, reverse

from django_yandex_intensive import settings

from . import forms
from . import models


def signup(request):
    template = 'users/signup.html'
    form = forms.SignUpForm(request.POST or None)
    context = {
        'form': form,
        'title': 'Регистрация'
    }
    if form.is_valid():
        user = form.save()
        if user.email:
            token = utils.generate_token(user.username, 12)
            activation_link = request.build_absolute_uri(
                reverse('users:activate', kwargs={
                    'token': token
                })
            )
            text = (
                f'Для активации вашего аккаунта перейдите по ссылке:\n'
                f'{activation_link}'
            )

            send_mail(
                'Activation',
                text,
                settings.EMAIL_ADDRESS,
                [user.email],
            )
        return redirect(reverse('homepage:home'))

    return render(request, template, context)


def activate_user(request, token):
    template = 'users/auth_message.html'
    title = 'Аккаунт успешно активирован'

    status, data = utils.decode_token(token)
    if status:
        encoded_user = User.objects.get(username=data['username'])
        if encoded_user.is_active:
            title = 'Этот аккаунт уже активирован'
        else:
            encoded_user.is_active = True
            encoded_user.save()
    else:
        title = data

    context = {
        'title': title
    }

    return render(request, template, context)


def user_list(request):
    template = 'users/user_list.html'
    users = models.ProxyUser.objects.get_active_users().all()
    context = {
        'users': users,
        'title': 'Список активных пользователей'
    }
    return render(request, template, context)


def user_detail(request, pk):
    template = 'users/user_detail.html'
    query_user = models.ProxyUser.objects.get_user_detail(pk)
    user = get_object_or_404(query_user)

    context = {
        'user': user,
        'title': 'Пользователь'
    }

    return render(request, template, context)


@login_required
def profile(request):
    user = request.user
    template = 'users/profile.html'
    user_form = forms.EditUserForm(
        request.POST or None,
        initial={
            'username': user.username,
            'email': user.email,
        },
        instance=user
    )
    birthday = user.profile.birthday
    if birthday:
        birthday = birthday.isoformat()

    profile_form = forms.EditProfileForm(
        request.POST or None,
        request.FILES or None,
        initial={
            'image': user.profile.image,
            'birthday': birthday,
        },
        instance=user.profile
    )

    if not user.is_authenticated:
        return redirect('users:login')

    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        return redirect('users:profile')

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Профиль',
        'coffee_count': user.profile.coffee_count,
    }
    return render(request, template, context)


def recover(request, token):
    template = 'users/auth_message.html'
    title = 'Аккаунт успешно восстановлен'
    status, data = utils.decode_token(token)

    if not status:
        title = data
    else:
        username = data['username']
        user = User.objects.filter(username=username).first()
        attempts = AccessAttempt.objects.filter(username=username).first()

        if not attempts:
            title = 'Аккаунт уже восстановлен'
        else:
            user.is_active = True
            user.save()
            attempts.delete()

    context = {
        'title': title
    }

    return render(request, template, context)
