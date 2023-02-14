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
            ('$123', 404), ('-1', 404), ('0', 200),
            ('-0', 404)
        ]
        for case, status in cases:
            with self.subTest(f'Test case: {case}, expected: {status}'):
                response = Client().get(f'/catalog/{case}')
                self.assertEqual(response.status_code, status)

    def test_positive_integer(self):
        cases = [
            ('0', 404), ('-1', 404), ('-9', 404), ('01', 404), ('-0', 404),
            ('1', 200), ('1000', 200), ('123456789', 200),
            ('asd', 404), ('-asd', 404), ('1asd', 404), ('asd123', 404),
        ]

        for case, status in cases:
            with self.subTest(f'Case: {case}, expected: {status}'):
                response = Client().get(f'/catalog/re/{case}')
                self.assertEqual(response.status_code, status)

    def test_converter(self):
        cases = [
            ('0', 404), ('-1', 404), ('-9', 404), ('01', 404), ('-0', 404),
            ('1', 200), ('1000', 200), ('123456789', 200),
            ('asd', 404), ('-asd', 404), ('1asd', 404), ('asd123', 404),
        ]

        for case, status in cases:
            with self.subTest(f'Case: {case}, expected: {status}'):
                response = Client().get(f'/catalog/converter/{case}')
                self.assertEqual(response.status_code, status)
