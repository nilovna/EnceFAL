# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    #(r'^$', include(admin.site.urls)),
    (r'^$', 'project.views.index'),
    (r'^admin/', include(admin.site.urls)),
    url(r'^employee/$', 'encefal.views.index_employee', name='index_employee'),
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

