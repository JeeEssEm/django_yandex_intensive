from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='users/auth_form.html',
            extra_context={
                'title': 'Вход в аккаунт'
            }),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(template_name='users/logout.html'),
        name='logout'
    ),
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='users/auth_form.html',
            extra_context={
                'title': 'Смена пароля'
            }
        ),
        name='password_change'
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='users/auth_message.html'
        ),
        name='password_change_done'
    ),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/auth_form.html',
            extra_context={
                'title': 'Восстановление пароля'
            }
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/auth_message.html'
        ),
        name='password_reset_done'
    ),
    path(
        'password_reset/confirm',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/auth_form.html',
        ),
        name='password_reset_confirm'
    ),
    path(
        'password_reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/auth_message.html'
        ),
        name='password_reset_complete'
    ),
]
