"""OSRSPG URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.views.static import serve

from OSRSPG import settings
# Django urls
from applications.common.views import handle404, HandleNoPermission

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Implemented urls
urlpatterns += [
    path('', include('applications.player.urls', namespace='player')),
    path('', include('applications.bingo.urls', namespace='bingo')),
    path('', include('applications.tile.urls', namespace='tile')),
    path('', include('applications.common.urls', namespace='common'))
]

# Media url
urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {
            "document_root": settings.MEDIA_ROOT,
        },
    ),
]

# Statis url
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Add favicon url
urlpatterns += [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon/favicon.ico')))
]

# Error pages
handler404 = handle404.as_view()
handler403 = HandleNoPermission.as_view()
