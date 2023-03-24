from django.contrib.auth import views as auth_views
from django.urls import path

from . import forms
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('activate/<str:token>', views.activate_user, name='activate'),
    path('profile/', views.profile, name='profile'),
    path('user_detail/<int:pk>', views.user_detail, name='user_detail'),
    path('user_list/', views.user_list, name='user_list'),
    path('recover/<str:token>', views.recover, name='recover'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='users/login.html',
            authentication_form=forms.LoginForm,
            extra_context={
                'title': 'Вход в аккаунт'
            }),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            template_name='users/auth_message.html'
        ),
        name='logout'
    ),
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='users/password_form.html',
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
            template_name='users/password_form.html',
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
        'password_reset/<uidb64>/<token>',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_form.html',
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
