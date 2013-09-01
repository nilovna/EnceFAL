# -*- encoding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic.base import RedirectView

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/$', RedirectView.as_view(url='/employee/')),
    url(r'^$', RedirectView.as_view(url='/employee/')),
    url(r'^employee/', include('encefal.urls')),
    url(r'^employee/', include(admin.site.urls)),
    url(r'^vendre/$', 'encefal.views.vendre', name='vendre'),
    url(r'^livres/$', 'encefal.views.livres', name='livres'),
    url(r'^livre/$', 'encefal.views.livre', name='livre'),
    url(r'^exemplaire/$', 'encefal.views.exemplaire', name='exemplaire'),
    url(r'^vendeur/$', 'encefal.views.vendeur', name='vendeur'),
    url(r'^rapport/$', 'encefal.views.rapport', name='rapport'),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_URL}),
    )

