# -*- encoding: utf-8 -*-
import datetime
import json
import urllib
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.db.models import Sum, Q
from django.db.models import Count, Min, Sum, Avg
from django.forms.formsets import formset_factory

from project.encefal.models import Facture, Livre, Vendeur, ETAT_LIVRE_CHOICES, Exemplaire, ISBN_DB_BASE_QUERY
from project.encefal.forms import ExemplaireForm,LivreVendreForm, VendeurForm
from django.conf import settings

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
                              {'facture':facture, 'livres':livres,
                              'total': prix['total']},
                              context_instance = RequestContext(request))

def vendre(request):
    livre_ids = request.GET.get('ids').split(',')
    livres = Livre.objects.filter(id__in=livre_ids)
    facture = Facture()
    facture.save()
    facture.livres = livres
    facture.save()
    return HttpResponseRedirect(reverse('paiement')+"?id=%s" % (facture.id))

def ajouter_livres(request):
    if request.method == 'POST':
        formset = formset_factory(LivreVendreFrom, request.POST) 
        if formset.is_valid():
          
            return HttpResponseRedirect('/thanks/') 
    else:
        formset = formset_factory(LivreVendreForm, extra=5)
        vendeur = VendeurForm()

    return render(request, 'encefal/employee/ajouter_livres.html', {
        'formset': formset,
        'vendeur': vendeur,
    }) 

def liste_livres(request):
    if request.method == "POST":
        return HttpResponseRedirect(reverse('admin:encefal_vendeur_changelist'))

    vendeur = Vendeur.objects.get(id=request.GET.get('id'))
    date = datetime.date.today()
    livres = Livre.objects.filter(vendeur=vendeur)
    prix = livres.filter(Q(etat=ETAT_LIVRE_CHOICES[1][0])|Q(etat=ETAT_LIVRE_CHOICES[2][0])| Q(etat=ETAT_LIVRE_CHOICES[3][0])).aggregate(total=Sum('prix'))
    return render_to_response('encefal/liste_livres.html',
                              {'vendeur':vendeur, 'livres':livres, 'date':date,
                              'total': prix['total']},
                              context_instance = RequestContext(request))
def livres(request):

    #TODO redefinier le default Manager pour quil ne retourne que les exemplaires en vente
    livres = Livre.objects.all().annotate(prix_moyen=Avg('exemplaires__prix'),\
                                          quantite=Count('exemplaires__id'))

    context = {
            'livres':livres,
            }

    return render_to_response('encefal/livres.html',
            context, context_instance = RequestContext(request))

def livre(request):

    assert('isbn' in request.GET)
    assert('nb' in request.GET)
    assert(len(request.GET['isbn']) in [10,13])

    reponse = None
    livre = None
    isbn = request.GET['isbn']
    nb = request.GET['nb']

    try:
        livre = Livre.objects.get(isbn=isbn)
    except Livre.DoesNotExist:
        pass

    if not livre:
        query = ISBN_DB_BASE_QUERY.format(settings.ISBNDB_API_KEY, isbn)
        reponse_query = json.load(urllib.urlopen(query))
        if 'error' not in reponse_query:
            reponse_query = reponse_query['data'][0]
            reponse = {'titre':reponse_query['title'],
                       'auteur':reponse_query['author_data'][0]['name'],
                       'nb':nb}

    else:
        reponse = {'titre':livre.titre,
                   'auteur':livre.auteur,
                   'nb':nb}

    if reponse:
        return HttpResponse(json.dumps(reponse), content_type="application/json")
    else:
        return HttpResponseNotFound()

def exemplaire(request):

    assert('identifiant' in request.GET)

    identifiant = request.GET['identifiant']

    try:
        exemplaire = Livre.objects.get(pk=identifiant)
    except Exemplaire.DoesNotExist:
        return HttpResponseNotFound()

    assert(exemplaire.livre)

    reponse = {
               'titre':exemplaire.livre.titre,
               'auteur':exemplaire.livre.auteur,
               'prix':exemplaire.prix,
               'isbn':exemplaire.livre.isbn
              }

    return HttpResponse(json.dumps(reponse), content_type="application/json")

def vendeur(request):

    assert('code' in request.GET)
    #TODO Problablement ajouter le lenght du code

    vendeur = None
    code = request.GET['code']

    try:
        vendeur = Vendeur.objects.get(code_carte_etudiante=code)
    except Vendeur.DoesNotExist:
        return HttpResponseNotFound()

    reponse = {'nom':vendeur.nom,
               'prenom':vendeur.prenom,
               'code_permanent':vendeur.code_permanent,
               'email':vendeur.email}
    
    return HttpResponse(json.dumps(reponse), content_type="application/json")

def detail_facture(request):
    if request.method == "POST":
        return HttpResponseRedirect(reverse('admin:encefal_facture_changelist'))

    facture = Facture.objects.get(id=request.GET.get('id'))
    livres = facture.livres.all()
    return render_to_response('encefal/detail_facture.html', {'facture':facture,
                              'livres': livres},
                              context_instance = RequestContext(request))


# Default employee index page
def index_employee(request):
    return render_to_response('encefal/employee/index.html', {},
                              RequestContext(request))

def add_exemplaire_employee(request):
    if request.method == 'POST':
        form = ExemplaireForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')
    else:
        form = ExemplaireForm()

    return render_to_response('encefal/employee/add_exemplaire.html', {
                                'form': form,
                              }, RequestContext(request))

def sell(request):
    return render_to_response('encefal/employee/sell.html', {})
