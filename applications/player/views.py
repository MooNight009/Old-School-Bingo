from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import FormView, RedirectView, TemplateView

from applications.player.forms import LoginForm, CreateUserForm
from applications.player.tokens import account_activation_token


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
        user = form.save()
        # user.is_active = False
        # user.save

        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']

        # user = authenticate(self.request, username=username, password=password)
        if user is not None:
            # Send confirmation email
            current_site = get_current_site(self.request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('layouts/mails/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(
                mail_subject,
                message,
                'info@oldschoolbingo.com',
                [form.cleaned_data['email']]
            )

            login(self.request, user)
        return super().form_valid(form)


class LogoutView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return reverse('common:homepage')


class AccountView(TemplateView):
    template_name = 'pages/player/account.html'

    def get_context_data(self, **kwargs):
        context = super(AccountView, self).get_context_data(**kwargs)

        return context


class ActivateView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, kwargs['token']):
            user.is_active = True
            user.save()
            login(self.request, user)
        return reverse('common:homepage')
