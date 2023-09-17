from django.urls import path

from applications.player.views import *

app_name= 'player'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('account', AccountView.as_view(), name='account'),
    path('activate/<uidb64>/<token>', ActivateView.as_view(), name='activate')
]