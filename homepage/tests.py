from catalog import models

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


class TemplatesTest(TestCase):
    fixtures = ['tag_fixture.json', 'category_fixture.json']

    @classmethod
    def setUpTestData(cls):
        cls.tags = models.Tag.objects.all()
        cls.categories = models.Category.objects.all()

    @classmethod
    def tearDownClass(cls):
        cls.tags.delete()
        cls.categories.delete()

    def test_item_is_on_main(self):
        name = 'item_name'
        self.item = models.Item(
            name=name,
            category=self.categories[0],
            text='роскошно',
            is_on_main=True
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(self.tags[0])

        response = Client().get('/')
        self.assertContains(response, name)

    def test_item_not_on_main(self):
        name = 'item_name'
        self.item = models.Item(
            name=name,
            category=self.categories[0],
            text='роскошно',
            is_on_main=False
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(self.tags[0])

        response = Client().get('/')
        self.assertNotContains(response, name)
