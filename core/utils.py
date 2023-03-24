import re
from datetime import datetime, timedelta, timezone

from axes.models import AccessAttempt

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, render, reverse

from django_yandex_intensive import settings

import jwt


def remove_html_tags(val):
    open_tag = '<[^>]*>'
    close_tag = r'</[^>]*>'

    val = re.sub(open_tag, '', val[::])
    val = re.sub(close_tag, '', val[::])

    return val


def generate_token(username, exp):
    exp = datetime.now(tz=timezone.utc) + timedelta(hours=exp)
    return jwt.encode(
        {
            'exp': exp,
            'username': username
        },
        settings.SECRET_KEY,
        algorithm='HS256'
    )


def decode_token(token):
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'],
                          verify=True)
    except jwt.exceptions.ExpiredSignatureError:
        return False, 'Время действия кода активации истекло'
    except jwt.exceptions.DecodeError:
        return False, 'Некорректная ссылка'
    return True, data


def lock_account(request, user):
    template = 'users/auth_message.html'
    context = {
        'title': 'Аккаунт заблокирован за многочисленные'
                 ' неудачные попытки входа. Для восстановления'
                 ' аккаунта перейдите по ссылке, отправленной вам на почту'
    }
    name = user['username']
    user_db = (
            User.objects.filter(email=name)
            | User.objects.filter(username=name)
    ).only('email', 'username').first()
    if user_db is None:
        return redirect('users:login')

    email = user_db.email
    username = user_db.username

    attempts = AccessAttempt.objects.filter(
        username=username).only('failures_since_start').first()

    if attempts.failures_since_start == settings.AXES_FAILURE_LIMIT:
        user_db.is_active = False
        user_db.save()

        token = generate_token(username, 7 * 24)
        link = request.build_absolute_uri(
            reverse('users:recover', kwargs={
                'token': token
            })
        )
        text = (
            f'Ваш аккаунт заблокирован за многочисленные неудачные'
            f' попытки входа. Для восстановления перейдите по ссылке:\n'
            f'{link}'
        )
        send_mail(
            'Восстановление аккаунта',
            text,
            settings.EMAIL_ADDRESS,
            [email],
        )

    return render(request, template, context)


def normalize_email(email):
    email = email.lower().strip()
    left_part = email.split('@')[0].replace('+', '')
    right_part = email.split('@')[1].replace('ya.ru', 'yandex.ru')

    if right_part == 'gmail.com':
        left_part = left_part.replace('.', '')
    elif right_part == 'yandex.ru':
        left_part = left_part.replace('.', '-')

    return left_part + '@' + right_part
