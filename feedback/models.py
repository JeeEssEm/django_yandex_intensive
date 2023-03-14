import django.db.models

import pathlib


class FeedBack(django.db.models.Model):

    class Statuses(django.db.models.TextChoices):
        received = 'received', 'получено'
        idle = 'idle', 'в процессе'
        answered = 'answered', 'ответ дан'

    def get_upload_folder(instance, filename):
        return pathlib.Path('upload_to') / str(instance.id) / filename

    text = django.db.models.TextField()
    created_on = django.db.models.DateTimeField(auto_now_add=True)
    email = django.db.models.EmailField()
    status = django.db.models.CharField(
        choices=Statuses.choices,
        default=Statuses.received,
        max_length=16
    )


class Attachment(django.db.models.Model):
    def get_upload_folder(instance, filename):
        return pathlib.Path('upload_to') / str(instance.feedback.id) / filename

    file = django.db.models.FileField(upload_to=get_upload_folder, null=True, blank=True)
    feedback = django.db.models.ForeignKey(
        to=FeedBack,
        on_delete=django.db.models.deletion.CASCADE,
        related_name='attachments'
    )
