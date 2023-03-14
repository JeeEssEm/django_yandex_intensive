import django.db.models


class FeedBack(django.db.models.Model):

    class Statuses(django.db.models.TextChoices):
        received = 'received', 'получено'
        idle = 'idle', 'в процессе'
        answered = 'answered', 'ответ дан'

    text = django.db.models.TextField()
    created_on = django.db.models.DateTimeField(auto_now_add=True)
    email = django.db.models.EmailField()
    status = django.db.models.CharField(
        choices=Statuses.choices,
        default=Statuses.received,
        max_length=16
    )
