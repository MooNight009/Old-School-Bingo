from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import FormView, RedirectView, TemplateView

from applications.player.forms import LoginForm, CreateUserForm, ForgotPasswordForm, ResetPasswordForm
from applications.player.tokens import account_activation_token


class LoginView(FormView):
    template_name = 'pages/player/login.html'
    form_class = LoginForm
    success_url = '/'

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

    def get_success_url(self):
        return reverse('player:registration_confirmation')

    def form_valid(self, form):
        user = form.save()
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


class ForgotPasswordView(FormView):
    template_name = 'pages/player/forgot_password.html'
    form_class = ForgotPasswordForm
    success_url = '/'

    def form_valid(self, form):
        user = User.objects.filter(email=form.cleaned_data['email']).first()

        # Send password reset email
        current_site = get_current_site(self.request)
        mail_subject = 'Password change in OldSchool Bingo'
        message = render_to_string('layouts/mails/password_reset.html', {
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

        return super().form_valid(form)


class ResetPasswordView(FormView):
    template_name = 'pages/player/reset_password.html'
    form_class = ResetPasswordForm
    success_url = '/'

    def form_valid(self, form):
        try:
            uid = force_str(urlsafe_base64_decode(self.kwargs['uidb64']))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, self.kwargs['token']):
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(self.request, user)

        return super().form_valid(form)

class RegistrationConfirmationView(TemplateView):
    template_name = 'pages/player/checkemail.html'

class ActivateView(RedirectView):
    """
        Activates the player's account
        TODO: Switch to features requiring account activation
    """

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
