from django.test import Client, TestCase
from django.urls import reverse

from parameterized import parameterized

from . import forms
from . import models


class FormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = forms.FeedBackForm()
        cls.form_data = {
            models.FeedBack.email.field.name: 'real@mail.not',
            models.FeedBack.text.field.name: 'some text',
        }

    @parameterized.expand([
        ('email', 'Email'),
        ('text', 'Текст'),
    ])
    def test_label_email(self, attr, expected):
        label = FormTest.form.fields[
            getattr(models.FeedBack, attr).field.name
        ].label
        self.assertEquals(label, expected)

    @parameterized.expand([
        ('email', 'Введите ваш email'),
        ('text', 'Введите текст вашей проблемы'),
    ])
    def test_help_text(self, attr, expected):
        label = FormTest.form.fields[
            getattr(models.FeedBack, attr).field.name
        ].help_text
        self.assertEquals(label, expected)

    def test_redirect(self):
        response = Client().post(
            reverse('feedback:feedback'),
            data=self.form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('feedback:thanks'))

    def test_form_in_context(self):
        response = Client().get(reverse('feedback:feedback'))
        self.assertIn('form', response.context)

    def test_db_form(self):
        feedback_count = models.FeedBack.objects.count()
        Client().post(
            reverse('feedback:feedback'),
            data=self.form_data,
            follow=True
        )
        self.assertEqual(feedback_count + 1, models.FeedBack.objects.count())
