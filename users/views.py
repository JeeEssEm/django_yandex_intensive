from datetime import datetime, timedelta, timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render, reverse

from django_yandex_intensive import settings

import jwt

from . import forms


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
            exp = datetime.now(tz=timezone.utc) + timedelta(hours=12)
            token = jwt.encode(
                {
                    'exp': exp,
                    'username': user.username
                },
                settings.SECRET_KEY,
                algorithm='HS256'
            )
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

    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'],
                          verify=True)
        encoded_user = User.objects.get(username=data['username'])
        if encoded_user.is_active:
            title = 'Этот аккаунт уже активирован'
        else:
            encoded_user.is_active = True
            encoded_user.save()
    except jwt.exceptions.ExpiredSignatureError:
        title = 'Время действия кода активации истекло'
    except jwt.exceptions.DecodeError:
        title = 'Некорректная ссылка'

    context = {
        'title': title
    }

    return render(request, template, context)


def user_list(request):
    template = 'users/user_list.html'
    users = User.objects.filter(is_active=True).only('username', 'id').all()
    context = {
        'users': users,
        'title': 'Список активных пользователей'
    }
    return render(request, template, context)


def user_detail(request, pk):
    template = 'users/user_detail.html'
    query_user = User.objects.filter(pk=pk).select_related('profile').only(
        'first_name',
        'last_name',
        'profile__image',
        'profile__birthday',
        'profile__coffee_count'
    )
    user = get_object_or_404(query_user)

    context = {
        'user_page': user,
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

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Профиль',
        'coffee_count': user.profile.coffee_count,
    }
    return render(request, template, context)
