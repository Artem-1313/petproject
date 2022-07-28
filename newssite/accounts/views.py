from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
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
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('newsapp:main')
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        user = authenticate(username=self.request.POST['username'], password=self.request.POST['password'])
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('newsapp:main')


class UserAccountInformation(LoginRequiredMixin, TemplateView):
    template_name = "accounts/user_account_information.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user
        return context