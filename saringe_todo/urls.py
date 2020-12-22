from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from drf_autodocs.views import TreeView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns_v1 = [
    url(r'^users/', include('users.urls')),
    url(r'^todos/', include('todo.urls')),
]

urlpatterns = [
    url(r'^$', TreeView.as_view(), name='api-tree'),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^admin/', admin.site.urls),
    url(r'^apiauth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/', include(urlpatterns_v1)),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
