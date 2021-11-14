"""cinema URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from decorator_include import decorator_include

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.views.decorators import user_passes_test

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', decorator_include(staff_member_required(login_url='/user/login'), include('admin.urls'))),
    path('user/', include('user.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)