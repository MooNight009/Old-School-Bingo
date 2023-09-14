from django.urls import path

from applications.common.views import HandleNoPermission, handle404

app_name = 'bingo'

urlpatterns = [
    path('no_permission', HandleNoPermission.as_view(), name='no_permission'),
    path('404', handle404.as_view(), name='404'),
]
