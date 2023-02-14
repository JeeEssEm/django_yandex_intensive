from django.test import Client, TestCase


class StaticUrlTest(TestCase):
    def test_catalog_list(self):
        response = Client().get('/catalog/')
        self.assertEqual(response.status_code, 200)

    def test_catalog_item(self):
        correct = [
            ('1', 200), ('123123123123', 200),
            ('0', 200), ('123#', 200),
        ]
        fail_test_numbers = [
            ('123asd', 404), ('-1', 404), ('-0', 404),
            ('$123', 404), ('123asd/asdew', 404),
        ]
        fail_test_strings = [
            ('asd', 404), ('catalog/1', 404),
            ('$#@', 404),
        ]
        cases = fail_test_strings + fail_test_numbers + correct
        for case, status in cases:
            with self.subTest(f'Test case: {case}, expected: {status}'):
                response = Client().get(f'/catalog/{case}')
                self.assertEqual(response.status_code, status)

    def test_positive_integer(self):
        fail_test_string = [
            ('asd', 404), ('-asd', 404),
            ('1asd', 404), ('asd123', 404),
        ]
        fail_test_numbers = [
            ('0', 404), ('-1', 404), ('-9', 404),
            ('01', 404), ('-0', 404),
        ]
        correct_nums = [
            ('1', 200), ('1000', 200),
            ('123456789', 200),
        ]

        cases = correct_nums + fail_test_numbers + fail_test_string
        for case, status in cases:
            with self.subTest(f'Case: {case}, expected: {status}'):
                response = Client().get(f'/catalog/re/{case}')
                self.assertEqual(response.status_code, status)

    def test_converter(self):
        fail_test_string = [
            ('-asd', 404), ('asd123', 404),
            ('1asd', 404), ('asd', 404),
        ]
        fail_test_numbers = [
            ('-1', 404), ('-9', 404), ('01', 404),
            ('-0', 404), ('0', 404),
        ]
        correct_nums = [
            ('1', 200), ('123456789', 200),
            ('1000', 200),
        ]

        cases = correct_nums + fail_test_numbers + fail_test_string

        for case, status in cases:
            with self.subTest(f'Case: {case}, expected: {status}'):
                response = Client().get(f'/catalog/converter/{case}')
                self.assertEqual(response.status_code, status)
