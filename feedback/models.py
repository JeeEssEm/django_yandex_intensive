import django.db.models


class FeedBack(django.db.models.Model):

    class Meta:
        verbose_name = 'обратная связь'
        verbose_name_plural = 'обратные связи'

    class Statuses(django.db.models.TextChoices):
        received = 'received', 'получено'
        idle = 'idle', 'в процессе'
        answered = 'answered', 'ответ дан'

    text = django.db.models.TextField('текст')
    created_on = django.db.models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    email = django.db.models.EmailField('email')
    status = django.db.models.CharField(
        'статус',
        choices=Statuses.choices,
        default=Statuses.received,
        max_length=16
    )

    def __str__(self):
        return 'Обратная связь'
