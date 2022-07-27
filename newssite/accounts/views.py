from django.shortcuts import render
from django.views.generic import FormView
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LogoutView
# Create your views here.

class RegisterUser(FormView):
    form_class = CustomUserCreationForm
    success_url = "/"
    template_name = "accounts/registration.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        return super(RegisterUser, self).form_valid(form)

class LoginUser(FormView):
    form_class = AuthenticationForm
    success_url = '/'
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        user = authenticate(username=self.request.POST['username'], password=self.request.POST['password'])
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)


class LogoutUser(LogoutView):

    redirect_field_name = 'index'
    template_name = "accounts/logout.html"