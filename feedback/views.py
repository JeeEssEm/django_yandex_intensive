from django.core.mail import send_mail
from django.shortcuts import redirect, render

from . import forms


def feedback(request):
    template = 'feedback/feedback.html'
    form = forms.FeedBackForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        email = form.cleaned_data.get('email')
        text = form.cleaned_data.get('text')
        send_mail(
            'Feedback',
            text,
            email,
            ['receiver@athlon.amd']
        )
        return redirect('feedback:thanks')

    return render(request, template, context)


def thanks(request):
    template = 'feedback/thanks.html'
    context = {}

    return render(request, template, context)
