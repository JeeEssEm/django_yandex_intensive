from django.test import Client, TestCase


class StaticUrlTest(TestCase):
    def test_homepage(self):
        response = Client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_teapot_status(self):
        response = Client().get('/coffee/')
        self.assertEqual(response.status_code, 418)

    def test_teapot_content(self):
        response = Client().get('/coffee/')
        self.assertContains(response, 'Я чайник', status_code=418)

