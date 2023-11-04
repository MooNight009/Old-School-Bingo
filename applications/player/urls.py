from django.urls import path

from applications.player.views import *

app_name = 'player'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('account', AccountView.as_view(), name='account'),
    path('forgot_password', ForgotPasswordView.as_view(), name='forgot_password'),
    path('activate/<uidb64>/<token>', ActivateView.as_view(), name='activate'),
    path('reset_password/<uidb64>/<token>', ResetPasswordView.as_view(), name='reset_password'),
    path('registration_confirmation/', RegistrationConfirmationView.as_view(), name='registration_confirmation')
]
