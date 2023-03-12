import django.db.models


class FeedBack(django.db.models.Model):
    text = django.db.models.TextField()
    created_on = django.db.models.DateTimeField(auto_now_add=True)
    email = django.db.models.EmailField()
