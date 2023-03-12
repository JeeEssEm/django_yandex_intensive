"""django_yandex_intensive URL Configuration

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
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path


from . import settings

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('catalog/', include('catalog.urls')),
    path('about/', include('about.urls')),
    path('feedback/', include('feedback.urls')),
    path('tinymce/', include('tinymce.urls')),
    prefix_default_language=False
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

    if hasattr(settings, 'MEDIA_ROOT'):
        urlpatterns += static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT
        )
    else:
        urlpatterns += staticfiles_urlpatterns()
