from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Examples:
    # url(r'^$', 'totmann.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', auth_views.login, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^check/', include('core.urls', namespace='core')),
    url(r'^web/', include('web.urls', namespace='web')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url('^', include('django.contrib.auth.urls'))
]
