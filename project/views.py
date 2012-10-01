# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect

def index(request):
    return redirect('/admin/')
    #return render_to_response('index.html', {}, RequestContext(request))
