import django.forms

from . import models


class FeedBackForm(django.forms.ModelForm):
    class Meta:
        model = models.FeedBack

        fields = (
            models.FeedBack.email.field.name,
            models.FeedBack.text.field.name,
        )
        labels = {
            models.FeedBack.email.field.name: 'Email',
            models.FeedBack.text.field.name: 'Текст',
        }

        help_texts = {
            models.FeedBack.email.field.name: 'Введите ваш email',
            models.FeedBack.text.field.name: 'Введите текст вашей проблемы',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
