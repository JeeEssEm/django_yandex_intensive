import django.core.exceptions
from django.test import Client, TestCase

from parameterized import parameterized

from . import models


class StaticUrlTest(TestCase):
    def test_catalog_list(self):
        response = Client().get('/catalog/')
        self.assertEqual(response.status_code, 200)

    def test_catalog_item(self):
        correct = [
            ('1', 200),
            ('123123123123', 200),
            ('0', 200),
            ('123#', 200),
        ]
        fail_test_numbers = [
            ('123asd', 404),
            ('-1', 404),
            ('-0', 404),
            ('$123', 404),
            ('123asd/asdew', 404),
        ]
        fail_test_strings = [
            ('asd', 404),
            ('catalog/1', 404),
            ('$#@', 404),
        ]
        cases = fail_test_strings + fail_test_numbers + correct
        for case, status in cases:
            with self.subTest(f'Test case: {case}, expected: {status}'):
                response = Client().get(f'/catalog/{case}')
                self.assertEqual(response.status_code, status)

    def test_positive_integer(self):
        fail_test_string = [
            ('asd', 404),
            ('-asd', 404),
            ('1asd', 404),
            ('asd123', 404),
        ]
        fail_test_numbers = [
            ('0', 404),
            ('-1', 404),
            ('-9', 404),
            ('01', 404),
            ('-0', 404),
        ]
        correct_nums = [
            ('1', 200),
            ('1000', 200),
            ('123456789', 200),
        ]

        cases = correct_nums + fail_test_numbers + fail_test_string
        for case, status in cases:
            with self.subTest(f'Case: {case}, expected: {status}'):
                response = Client().get(f'/catalog/re/{case}')
                self.assertEqual(response.status_code, status)

    def test_converter(self):
        fail_test_string = [
            ('-asd', 404),
            ('asd123', 404),
            ('1asd', 404),
            ('asd', 404),
        ]
        fail_test_numbers = [
            ('-1', 404),
            ('-9', 404),
            ('01', 404),
            ('-0', 404),
            ('0', 404),
        ]
        correct_nums = [
            ('1', 200),
            ('123456789', 200),
            ('1000', 200),
        ]

        cases = correct_nums + fail_test_numbers + fail_test_string

        for case, status in cases:
            with self.subTest(f'Case: {case}, expected: {status}'):
                response = Client().get(f'/catalog/converter/{case}')
                self.assertEqual(response.status_code, status)


class ModelsTests(TestCase):
    fixtures = ['category_new_fixture.json', 'tag_new_fixture.json']

    @classmethod
    def setUpTestData(cls):
        cls.categories = models.Category.objects.all()
        cls.tags = models.Tag.objects.all()

    @classmethod
    def tearDownClass(cls):
        cls.categories.delete()
        cls.tags.delete()

    # тестирование модели category
    @parameterized.expand(
        [(-1,), (-32323212,), (32768,), (999999,), (1000000,), (0,)]
    )
    def test_wrong_weight_category(self, weight):
        category_count = models.Category.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            self.cat = models.Category(
                name='test', slug='some-correct-slug', weight=weight
            )
            self.cat.full_clean()
            self.cat.save()

        self.assertEqual(models.Category.objects.count(), category_count)

    @parameterized.expand([(1,), (123,), (32767,), (9999,), (4,), (12312,)])
    def test_correct_weight_category(self, weight):
        category_count = models.Category.objects.count()
        self.cat = models.Category(
            name='test', slug='some-correct-slug', weight=weight,
        )
        self.cat.validate_unique()
        self.cat.full_clean()
        self.cat.save()

        self.assertEqual(models.Category.objects.count(), category_count + 1)

    @parameterized.expand(
        [
            ('asd-%',),
            ('$lug-_',),
            ('a' * 201,),
            ('',),
            ('читаемый-человеком',),
        ]
    )
    def test_wrong_slug_category(self, slug):
        category_count = models.Category.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.cat = models.Category(name='test', slug=slug, weight=100)

            self.cat.full_clean()
            self.cat.save()

        self.assertEqual(models.Category.objects.count(), category_count)

    @parameterized.expand(
        [
            ('asd-asd',),
            ('some-correct-slug',),
        ]
    )
    def test_correct_slug_category(self, slug):
        category_count = models.Category.objects.count()
        self.cat = models.Category(
            name='test',
            slug=slug,
            weight=100,
            )
        self.cat.validate_unique()
        self.cat.full_clean()
        self.cat.save()

        self.assertEqual(models.Category.objects.count(), category_count + 1)

    def test_duplicate_slug_category(self):
        category_count = models.Category.objects.count()
        self.cat = models.Category(
            name='test',
            slug='normal-slug',
            weight=100,
            )
        self.cat.validate_unique()
        self.cat.full_clean()
        self.cat.save()

        with self.assertRaises(django.core.exceptions.ValidationError):
            self.cat1 = models.Category(
                name='test123', slug='normal-slug', weight=100
            )
            self.cat1.full_clean()
            self.cat1.save()

        self.assertEqual(category_count + 1, models.Category.objects.count())

    # тестирование модели item
    @parameterized.expand([
            ('превосходно приготовленный',),
            ('роскошно посоленный',),
            ('роскошно',),
            ('превосходно',)
        ])
    def test_correct_item_text(self, text):
        items_count = models.Item.objects.count()
        self.item = models.Item(
            name='some name', category=self.categories[0], text=text,
        )
        self.item.validate_unique()
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(self.tags[0])

        self.assertEqual(models.Item.objects.count(), items_count + 1)

    @parameterized.expand([
        ('приготовленный',),
        ('посоленный',),
        ('роскошный',),
        ('прекрасно',),
        ('роскошноооы',),
        ('препревосходно',),
        ('превосходночень',),
    ])
    def test_wrong_item_text(self, text):
        items_count = models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = models.Item(
                name='some name', category=self.categories[0], text=text
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(self.tags[0])

        self.assertEqual(models.Item.objects.count(), items_count)

    @parameterized.expand(
        [
            ('',),
            ('a' * 151,),
            ('ab' * 76,),
        ]
    )
    def test_wrong_item_name(self, name):
        items_count = models.Item.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = models.Item(
                name=name, category=self.categories[0], text='роскошно'
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(self.tags[0])

        self.assertEqual(models.Item.objects.count(), items_count)

    @parameterized.expand(
        [
            ('какое-то имя',),
            ('ab',),
            ('some long but not name',),
        ]
    )
    def test_correct_item_name(self, name):
        items_count = models.Item.objects.count()

        self.item = models.Item(
            name=name, category=self.categories[0], text='превосходно',
        )
        self.item.validate_unique()
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(self.tags[0])

        self.assertEqual(models.Item.objects.count(), items_count + 1)

    # тестирование модели tag
    @parameterized.expand(
        [
            ('asd-%',),
            ('$lug-_',),
            ('a' * 201,),
            ('',),
            ('читаемый-человеком',),
        ]
    )
    def test_wrong_slug_tag(self, slug):
        tag_count = models.Tag.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.tag = models.Tag(
                name='test',
                slug=slug,
            )

            self.tag.full_clean()
            self.tag.save()

        self.assertEqual(models.Tag.objects.count(), tag_count)

    @parameterized.expand(
        [
            ('asd-asd',),
            ('some-correct-slug',),
        ]
    )
    def test_correct_slug_tag(self, slug):
        tag_count = models.Tag.objects.count()
        self.tag = models.Tag(
            name='test',
            slug=slug,
        )
        self.tag.validate_unique()
        self.tag.full_clean()
        self.tag.save()

        self.assertEqual(models.Tag.objects.count(), tag_count + 1)

    def test_normalized(self):
        tag_count = models.Tag.objects.count()

        self.correct_tag = models.Tag(
            name='balance',
            slug='slugg',
        )
        self.correct_tag.validate_unique()
        self.correct_tag.full_clean()
        self.correct_tag.save()

        with self.assertRaises(django.core.exceptions.ValidationError):
            self.wrong_tag = models.Tag(
                name='bаlаnce',
                slug='slug',
            )
            self.wrong_tag.validate_unique()
            self.wrong_tag.full_clean()
            self.wrong_tag.save()

        self.assertEqual(models.Tag.objects.count(), tag_count + 1)
