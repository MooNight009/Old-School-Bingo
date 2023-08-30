from django.urls import path

from applications.defaults.views import HomePageView

app_name= 'defaults'

urlpatterns = [
    path('', HomePageView.as_view(), name='main'),
]