from django.conf.urls import patterns, include, url


urlpatterns = patterns('document.views',
    url(r'edit/(?P<document_id>\d+)/$', 'edit_document'),
    url(r'document/(?P<document_id>\d+)/$', 'document'),
    url(r'all/$', 'all_documents'),
    url(r'new/$', 'create_document'),
    url(r'^$', 'all_documents'),
)
