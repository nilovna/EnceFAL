# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^$', 'project.views.index'),
    (r'^admin/', include(admin.site.urls)),
    url(r'^paiement/$', 'encefal.views.paiement', name='paiement'), 
    url(r'^vendre/$', 'encefal.views.vendre', name='vendre'),   
    url(r'^liste_livres/$', 'encefal.views.liste_livres', name='liste_livres'),   
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

