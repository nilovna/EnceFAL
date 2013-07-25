# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('encefal.views',
    url(r'^$', 'index_employee', name='employee_home'),
    url(r'^add_exemplaire$', 'add_exemplaire_employee',
        name='add_exemplaire'),
    url(r'^ajouter_livres', 'ajouter_livres',
        name='ajouter_livres'),
    url(r'^sell$', 'sell', name='sell'),
)
