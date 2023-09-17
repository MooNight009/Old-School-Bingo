from django.urls import path

from applications.common.views import *

app_name = 'common'

urlpatterns = [
    path('no_permission', HandleNoPermission.as_view(), name='no_permission'),
    path('404', handle404.as_view(), name='404'),
    path('main', BingosView.as_view(), name='main'),
    path('', HomePageView.as_view(), name='homepage')
]
