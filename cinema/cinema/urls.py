from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from decorator_include import decorator_include
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', decorator_include(staff_member_required(login_url='/user/login'), include('admin.urls'))),
    path('user/', include('user.urls')),
    path(r'^i18n/', include('django.conf.urls.i18n')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
