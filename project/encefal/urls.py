# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('encefal.views',
    url(r'^$', 'index_employee', name='employee_home'),
)
