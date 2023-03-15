import django.forms

from . import models


class FeedBackForm(django.forms.ModelForm):
    attachments = django.forms.FileField(
        widget=django.forms.ClearableFileInput(
            attrs={
                'multiple': True
            }
        ),
        label='Вложения',
        help_text='Добавьте вложения',
        required=False
    )
    name = django.forms.CharField(
        label='Имя',
        help_text='Введите ваше имя',
        max_length=64
    )
    email = django.forms.EmailField(
        label='Email',
        help_text='Введите ваш email',
    )

    class Meta:
        model = models.FeedBack

        fields = (
            models.FeedBack.text.field.name,
        )
        labels = {
            models.FeedBack.text.field.name: 'Текст',
        }

        help_texts = {
            models.FeedBack.text.field.name: 'Введите текст вашей проблемы',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = models.User.objects.filter(
            email=self.cleaned_data['email']
        ).first()
        if not user:
            user = models.User.objects.create(
                email=self.cleaned_data['email'],
                name=self.cleaned_data['name'],
            )
        instance = super().save(commit=False)
        user.feedbacks.add(instance, bulk=False)
        instance.save()

        return instance
