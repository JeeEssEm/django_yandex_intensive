from django.shortcuts import render, redirect, reverse

from . import forms
from django_yandex_intensive import settings


def signup(request):
    template = 'users/auth_form.html'
    form = forms.SignUpForm(request.POST or None)
    context = {
        'form': form,
        'title': 'Регистрация'
    }
    if form.is_valid():

        return redirect(reverse('homepage:home'))

    return render(request, template, context)


def activate_user(request):
    ...
