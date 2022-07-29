from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import EmailInput, TextInput, PasswordInput
from django.http import HttpResponse
from django.shortcuts import redirect

from .models import NewUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = NewUser
        fields = ('email', 'first_name', 'last_name')



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = NewUser
        fields = ('first_name', 'last_name')


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': ("Email не зареєстровано або підтверджений! Перевірте пошту!"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})



