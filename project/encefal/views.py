# -*- encoding: utf-8 -*-
import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Sum

from project.encefal.models import Facture, Livre, Vendeur, ETAT_LIVRE_CHOICES

def index(request):
    return render_to_response('admin', {}, 
                                RequestContext(request))

def paiement(request):
    facture = Facture.objects.get(id=request.GET.get('id'))
    livres = facture.livres.all()
    if request.method == "POST":
        for livre in livres:
            # Changer le statut des livres à vendu.
            livre.etat = ETAT_LIVRE_CHOICES[1][0]
            livre.save()
        return HttpResponseRedirect(reverse('admin:encefal_livre_changelist'))
    else:
        prix = livres.aggregate(total=Sum('prix'))

    return render_to_response('encefal/paiement.html', 
                {'facture':facture, 'livres':livres, 'total': prix['total']}, 
                                context_instance = RequestContext(request))

def vendre(request):
    livre_ids = request.GET.get('ids').split(',')
    livres = Livre.objects.filter(id__in=livre_ids)
    facture = Facture()
    facture.save()
    facture.livres = livres
    facture.save()
    return HttpResponseRedirect(reverse('paiement')+"?id=%s" % (facture.id))
  
def liste_livres(request):
    if request.method == "POST":
        return HttpResponseRedirect(reverse('admin:encefal_vendeur_changelist'))

    vendeur = Vendeur.objects.get(id=request.GET.get('id'))
    date = datetime.date.today()
    livres = Livre.objects.filter(vendeur=vendeur)
    return render_to_response('encefal/liste_livres.html', 
                {'vendeur':vendeur, 'livres':livres, 'date':date}, 
                                context_instance = RequestContext(request))

    
