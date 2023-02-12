from django.test import Client, TestCase


class StaticUrlTest(TestCase):
    def test_catalog_list(self):
        response = Client().get('/catalog/')
        self.assertEqual(response.status_code, 200)

    def test_catalog_item_int(self):
        response = Client().get('/catalog/1')
        self.assertEqual(response.status_code, 200)

    def test_catalog_item_str(self):
        response = Client().get('/catalog/asd')
        self.assertEqual(response.status_code, 404)
