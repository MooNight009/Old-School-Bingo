from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.urls import reverse
from django.views.generic import FormView, RedirectView

from applications.player.forms import LoginForm, CreateUserForm


class LoginView(FormView):
    template_name = 'pages/player/login.html'
    form_class = LoginForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context)
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class RegisterView(FormView):
    template_name = 'pages/player/register.html'
    form_class = CreateUserForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']

        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class LogoutView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return reverse('defaults:main')
