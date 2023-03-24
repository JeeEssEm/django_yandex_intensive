from core import utils

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from django_yandex_intensive import settings

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
        token = utils.generate_token(self.not_active_user.username, 12)
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
                'email': self.user.email,
                'username': self.user.username + 'a',
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

    def test_ban(self):
        active_users = User.objects.filter(is_active=True).count()
        for _ in range(settings.AXES_FAILURE_LIMIT):
            self.client.post(
                reverse('users:login'),
                data={
                    'username': self.user.username,
                    'password': 'hbjbjbhjkbn123123'
                },
                follow=True
            )
        self.assertEqual(active_users - 1,
                         User.objects.filter(is_active=True).count())

    def test_recover(self):
        for _ in range(settings.AXES_FAILURE_LIMIT):
            self.client.post(
                reverse('users:login'),
                data={
                    'username': self.user.username,
                    'password': 'hbjbjbhjkbn123123'
                },
                follow=True
            )
        token = utils.generate_token(self.user.username, 7 * 24)
        self.client.get(
            reverse(
                'users:recover',
                kwargs={
                    'token': token
                }
            )
        )
        self.assertEqual(self.user.is_active, True)

    @parameterized.expand([
        ('john-week@yandex.ru', 'john.week@yandex.ru'),
        ('john-week@yandex.ru', 'john-week@ya.ru'),
        ('johnweek@gmail.com', 'john.week@gmail.com'),
        ('john+we+ek@gmail.com', 'johnweek@gmail.com'),
        ('john+we+ek@gmail.com', 'johnweek@gmail.com'.upper()),
    ])
    def test_normalize_email(self, email1, email2):
        users_count = User.objects.count()
        Client().post(
            reverse('users:signup'),
            data={
                'username': email1.split('@')[0],
                'email': email1,
                'password1': 'hbjbjbhjkbn123123',
                'password2': 'hbjbjbhjkbn123123'
            },
            follow=True
        )
        Client().post(
            reverse('users:signup'),
            data={
                'username': email2.split('@')[0],
                'email': email2,
                'password1': 'hbjbjbhjkbn123123',
                'password2': 'hbjbjbhjkbn123123'
            },
            follow=True
        )
        self.assertEqual(users_count + 1, User.objects.count())
