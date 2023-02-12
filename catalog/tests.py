from django.test import Client, TestCase


class StaticUrlTest(TestCase):
    def test_catalog_list(self):
        response = Client().get('/catalog/')
        self.assertEqual(response.status_code, 200)

    def test_catalog_item(self):
        cases = [
            ('1', 200), ('123123123123', 200),
            ('asd', 404), ('catalog/1', 404), ('123asd', 404),
            ('123asd/asdew', 404), ('$#@', 404), ('123#', 200),
            ('$123', 404), ('catalog/-1', 404)
        ]
        for case, status in cases:
            with self.subTest(f'Test case: {case}, expected: {status}'):
                response = Client().get(f'/catalog/{case}')
                self.assertEqual(response.status_code, status)
