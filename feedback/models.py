import pathlib

import django.db.models


class User(django.db.models.Model):
    email = django.db.models.EmailField()
    name = django.db.models.CharField(max_length=64)

    def __str__(self):
        return self.email


class FeedBack(django.db.models.Model):

    class Meta:
        verbose_name = 'обратная связь'
        verbose_name_plural = 'обратные связи'

    class Statuses(django.db.models.TextChoices):
        received = 'received', 'получено'
        idle = 'idle', 'в процессе'
        answered = 'answered', 'ответ дан'

    user = django.db.models.ForeignKey(
        to=User,
        on_delete=django.db.models.deletion.CASCADE,
        related_name='feedbacks'
    )
    text = django.db.models.TextField('текст')
    created_on = django.db.models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    status = django.db.models.CharField(
        'статус',
        choices=Statuses.choices,
        default=Statuses.received,
        max_length=16
    )

    def __str__(self):
        return self.text


class Attachment(django.db.models.Model):
    class Meta:
        verbose_name = 'вложение'
        verbose_name_plural = 'вложения'

    def get_upload_folder(instance, filename):
        return pathlib.Path('upload_to') / str(instance.feedback.id) / filename

    file = django.db.models.FileField(
        'вложение',
        upload_to=get_upload_folder,
        null=True,
        blank=True
    )
    feedback = django.db.models.ForeignKey(
        to=FeedBack,
        on_delete=django.db.models.deletion.CASCADE,
        related_name='attachments'
    )

    def __str__(self):
        return 'Вложения'
