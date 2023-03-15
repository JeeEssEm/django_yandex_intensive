from django.core.mail import send_mail
from django.shortcuts import redirect, render

from django_yandex_intensive import settings

from . import forms
from . import models


def feedback(request):
    template = 'feedback/feedback.html'
    form = forms.FeedBackForm(
        data=request.POST or None,
        files=request.FILES or None
    )
    context = {
        'form': form
    }
    if form.is_valid():
        email = form.cleaned_data.get('email')
        text = form.cleaned_data.get('text')
        attachments = request.FILES.getlist('attachments')
        send_mail(
            'Feedback',
            text,
            settings.EMAIL_ADDRESS,
            [email]
        )
        feedback_object = form.save()
        for file in attachments:
            models.Attachment.objects.create(
                file=file,
                feedback=feedback_object
            )
        return redirect('feedback:thanks')

    return render(request, template, context)


def thanks(request):
    template = 'feedback/thanks.html'
    context = {}

    return render(request, template, context)
