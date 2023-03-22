import shutil
import tempfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from parameterized import parameterized

from . import forms
from . import models

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class FormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = forms.FeedBackForm()
        cls.form_data = {
            'email': 'real@mail.not',
            'text': 'some text',
            'name': 'name',
            'attachments': ''
        }

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    @parameterized.expand([
        ('text', 'Текст'),
    ])
    def test_label_email(self, attr, expected):
        label = FormTest.form.fields[
            getattr(models.FeedBack, attr).field.name
        ].label
        self.assertEquals(label, expected)

    @parameterized.expand([
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

    def test_file_loading(self):
        attach = BytesIO(b'some text')
        attach.name = 'file_name.txt'
        form_data = self.form_data.copy()

        form_data['attachments'] = [
            SimpleUploadedFile(
                attach.name, attach.read()
            )
        ]
        Client().post(
            reverse('feedback:feedback'),
            data=form_data,
            follow=True
        )
        feedback = models.FeedBack.objects.filter(
            user__email=form_data['email']
        ).first()
        for file in feedback.attachments.all():
            with self.subTest('File does not created!'):
                self.assertTrue(
                    file.file.field.storage.exists(file.file.name)
                )

    def test_status(self):
        response = Client().post(
            reverse('feedback:feedback'),
            data=self.form_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
