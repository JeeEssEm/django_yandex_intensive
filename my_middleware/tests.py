from django.test import Client, TestCase, modify_settings


def get_nth_page(client, n, url):
    for _ in range(n - 1):
        client.get(url)
    return client.get(url)


class MiddlewareTest(TestCase):
    def test_urls(self):
        """ проверка на работу с разными url """
        client = Client()

        urls = [
            ('/catalog/', 'ацинартС с имаравот', 200),
            ('/coffee/', 'Я кинйач', 418),
            ('/about/', 'О еткеорп', 200),
        ]
        for url, result, code in urls:
            with self.subTest(f'Test url: {url} expected: {result}'):
                response = get_nth_page(client, 10, url)
                self.assertContains(response, result, status_code=code)

    def test_nums(self):
        """ проверка на срабатывание цифры """
        client = Client()

        urls = [
            ('/catalog/re/123', '123', 200),
            ('/catalog/converter/123', '123', 200),
        ]

        for url, result, code in urls:
            with self.subTest(f'Test url: {url} expected: {result}'):
                response = get_nth_page(client, 10, url)
                self.assertContains(response, result, status_code=code)

    def test_many_requests(self):
        """ проверка на срабатанывание на каждый 10 запрос """
        client = Client()
        response = get_nth_page(client, 100, '/catalog/')
        self.assertContains(response, 'ацинартС с имаравот')

    @modify_settings(MIDDLEWARE={
        'remove': 'my_middleware.middleware.ReverseMiddleware'
    })
    def test_disabled(self):
        client = Client()
        response = get_nth_page(client, 10, '/catalog/')
        self.assertContains(response, 'Страница с товарами')

    def test_request_other_urls(self):
        """ проверка запросов на разные url """
        client = Client()
        get_nth_page(client, 5, '/catalog/123')
        response = get_nth_page(client, 5, '/about/')
        self.assertContains(response, 'О еткеорп')

    def test_not_russian(self):
        client = Client()
        response = get_nth_page(client, 10, '')
        rs = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit,'
        self.assertContains(response, rs)
