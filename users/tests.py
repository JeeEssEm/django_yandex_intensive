from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from django_yandex_intensive import settings

import jwt

from parameterized import parameterized


class UsersTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.signup_form = {
            'email': 'test@host.com',
            'username': 'testuser',
            'password1': 'pwd123asd',
            'password2': 'pwd123asd'
        }
        cls.user = User.objects.create_user(
            username='user',
            email='active@host.com',
            password='asdasd123',
            is_active=True
        )
        cls.not_active_user = User.objects.create_user(
            username='test_user',
            email='test@hostmail.com',
            password='asdasd123',
            is_active=False
        )

    def test_signup(self):
        users_count = User.objects.count()
        Client().post(
            reverse('users:signup'),
            data=self.signup_form,
            follow=True
        )
        self.assertEqual(users_count + 1, User.objects.count())

    def test_activate(self):
        """ ну тут никак время для jwt токенов не замокать, потому что в
        библиотеке время для "exp" бёрется так "now = timegm(datetime.now(
        tz=timezone.utc).utctimetuple())". Замокать саму datetime нельзя,
        ошибку выкидывает, замокать return_value для jwt.decode тоже бред: в
        чём тогда смысл вообще отправлять токен в тесте, если я знаю,
        что jwt.decode вернёт 'правильные' данные, которые никак не сломать.
        Короче, я пытался замокать время, но не получилось. Оставлю рабочий
        вариант с utcnow, т.к. jwt берёт текущее время по UTC+0, сломать
        можно только если timedelta убрать или username выкинуть из payload
        (про смену алгоритма шифрования или
        смену секретного ключа вообще молчу)
        """
        active_users = User.objects.filter(is_active=True).count()
        exp = datetime.utcnow() + timedelta(hours=12)

        token = jwt.encode(
            {
                'exp': exp,
                'username': self.not_active_user.username,
            },
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        self.client.get(
            reverse(
                'users:activate',
                kwargs={
                    'token': token
                }
            )
        )
        self.assertEqual(active_users + 1,
                         User.objects.filter(is_active=True).count())

    def test_unique_email(self):
        users_count = User.objects.count()
        Client().post(
            reverse('users:signup'),
            data={
                'username': self.user.username,
                'password1': 'pwd123asd',
                'password2': 'pwd123asd'
            },
            follow=True
        )
        self.assertEqual(users_count, User.objects.count())

    @parameterized.expand([
        ('user',),
        ('active@host.com',)
    ])
    def test_login(self, username):
        response = self.client.post(
            reverse('users:login'),
            data={
                'username': username,
                'password': 'asdasd123'
            },
            follow=True
        )
        self.assertEqual(response.context['user'], self.user)
