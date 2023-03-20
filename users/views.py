from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User

from . import forms


def signup(request):
    template = 'users/auth_form.html'
    form = forms.SignUpForm(request.POST or None)
    context = {
        'form': form,
        'title': 'Регистрация'
    }
    if form.is_valid():
        form.save()
        return redirect(reverse('homepage:home'))

    return render(request, template, context)


def activate_user(request):
    ...


def user_list(request):
    template = 'users/user_list.html'
    users = User.objects.filter(is_active=True).all()
    context = {
        'users': users
    }
    return render(request, template, context)


def profile(request, pk):
    query_user = User.objects.filter(pk=pk)
    template = 'users/user_detail.html'
    user = get_object_or_404(
        query_user
    )
    context = {
        'user': user
    }
    return render(request, template, context)
