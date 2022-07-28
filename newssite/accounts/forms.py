from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect

from .models import NewUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = NewUser
        fields = ('email', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = NewUser
        fields = ('email',)



class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': ("Email не зареєстровано або підтверджений! Перевірте пошту!"),
    }



