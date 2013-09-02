# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('encefal.views',
    url(r'^$', 'acceuil', name='acceuil'),
    url(r'^vendre/$', 'vendre', name='vendre'),
    url(r'^livres/$', 'livres', name='livres'),
    url(r'^livre/$', 'livre', name='livre'),
    url(r'^exemplaire/$', 'exemplaire', name='exemplaire'),
    url(r'^vendeur/$', 'vendeur', name='vendeur'),
    url(r'^rapport/$', 'rapport', name='rapport'),
)
