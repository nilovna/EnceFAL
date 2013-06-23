# -*- encoding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    (r'^$', include(admin.site.urls)),
    (r'^admin/', include(admin.site.urls)),
    (r'^employee/', include('encefal.urls')),
    url(r'^paiement/$', 'encefal.views.paiement', name='paiement'),
    url(r'^vendre/$', 'encefal.views.vendre', name='vendre'),
    url(r'^livres/$', 'encefal.views.livres', name='livres'),
    url(r'^liste_livres/$', 'encefal.views.liste_livres', name='liste_livres'),
    url(r'^detail_facture/$', 'encefal.views.detail_facture', name='detail_facture'),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

