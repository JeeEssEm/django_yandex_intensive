import django.forms


class SignUpForm(django.forms.Form):
    login = django.forms.CharField(label='Логин')
    password = django.forms.CharField(
        widget=django.forms.PasswordInput(),
        label='Пароль'
    )
    repeat_password = django.forms.CharField(
        widget=django.forms.PasswordInput(),
        label='Повторите пароль'
    )

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if password != repeat_password:
            raise django.forms.ValidationError(
                'Пароли не совпадают'
            )
