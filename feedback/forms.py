import django.forms

from . import models


class FeedBackForm(django.forms.ModelForm):
    class Meta:
        model = models.FeedBack

        fields = (
            models.FeedBack.email.field.name,
            models.FeedBack.text.field.name,
            models.FeedBack.attachments.field.name,
        )
        labels = {
            models.FeedBack.email.field.name: 'Email',
            models.FeedBack.text.field.name: 'Текст',
            models.FeedBack.attachments.field.name: 'Вложения',
        }

        help_texts = {
            models.FeedBack.email.field.name: 'Введите ваш email',
            models.FeedBack.text.field.name: 'Введите текст вашей проблемы',
            models.FeedBack.attachments.field.name: 'Добавьте вложения',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
        self.fields[models.FeedBack.attachments.field.name].widget = (
            django.forms.ClearableFileInput(attrs={
                'multiple': True
            })
        )
