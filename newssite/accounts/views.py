from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import FormView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import tokenGenerator
# Create your views here.
User = get_user_model()


class RegisterUser(FormView):
    form_class = CustomUserCreationForm
    success_url = "/"
    template_name = "accounts/registration.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Активація акаунту!'
        message = render_to_string('accounts/activate_user.html',{
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'token': tokenGenerator.make_token(user)
        })
        email = EmailMessage(
            subject=mail_subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email]
        )
        email.send()

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

def activate_user(request, uidb64, token):

    print((uidb64))
    print(urlsafe_base64_decode(uidb64))
    # print(User.objects.get(pk=18))
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(user)
    except Exception as e:
        print(e,"ayayayaya")
        user=None
    if user and tokenGenerator.check_token(user, token):
        user.is_active = True
        print("asdsadsaddasdasdsadsadsadsadsadasd")
        user.save()
        return redirect(('accounts:login'))
    return render(request, "accounts/activate_user_failed.html")