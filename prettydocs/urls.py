from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Authentication:
    url(r'^login/$', 'auth.views.login_wrapper'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^passwd/reset/$', 'django.contrib.auth.views.password_reset'),
    url(r'^passwd/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^passwd/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^passwd/reset/complete/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^passwd/change/$', 'django.contrib.auth.views.password_change'),
    url(r'^passwd/change/done/$', 'django.contrib.auth.views.password_change_done'),
    url(r'^accounts/profile/$', 'auth.views.profile'),
    #apps
    url(r'^document/', include('document.urls')),
    url(r'^$', include('document.urls')),
    #admin
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)