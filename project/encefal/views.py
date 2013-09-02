# -*- encoding: utf-8 -*-
import datetime
import json
import urllib

from datetime import datetime as dt # est utilisé dans la views  rapport_date
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.http import (
                         HttpResponseRedirect,
                         HttpResponse, 
                         HttpResponseNotFound
                        )
from django.core.urlresolvers import reverse
from django.db.models import Sum, Q
from django.db.models import Count, Min, Sum, Avg
from django.forms.formsets import formset_factory

from project.encefal.models import (
                                    Facture, 
                                    Livre, 
                                    Vendeur, 
                                    ETAT_LIVRE_CHOICES, 
                                    Exemplaire, 
                                    ISBN_DB_BASE_QUERY
                                   )
from django.conf import settings

def index(request):
    return render_to_response('admin', {},
                              RequestContext(request))
    
def acceuil(request):
    return render_to_response('index.html', {},
                              RequestContext(request))

def vendre(request):
    livre_ids = request.GET.get('ids').split(',')
    livres = Livre.objects.filter(id__in=livre_ids)
    facture = Facture()
    facture.save()
    facture.livres = livres
    facture.save()
    return HttpResponseRedirect(reverse('paiement')+"?id=%s" % (facture.id))

def livres(request):

    livres = Livre.objects.all()
    livres = [livre for livre in livres if livre.nb_exemplaires_en_vente()]

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
    assert('nb' in request.GET)

    nb = request.GET['nb']
    identifiant = request.GET['identifiant']

    try:
        exemplaire = Exemplaire.objects.get(pk=identifiant)
    except Exemplaire.DoesNotExist:
        return HttpResponseNotFound()
    
    assert(exemplaire.livre)

    if exemplaire.etat != 'VENT':
        reponse = {
                   'status':'error',
                   'message':"L'exemplaire n'est pas en vente"
                  }
    else:
        reponse = {
                   'status':'ok',
                   'titre':exemplaire.livre.titre,
                   'auteur':exemplaire.livre.auteur,
                   'prix':int(exemplaire.prix),
                   'isbn':exemplaire.livre.isbn,
                   'nb':nb
                  }

    return HttpResponse(json.dumps(reponse), content_type="application/json")

def vendeur(request):

    assert('code' in request.GET)
    #TODO Problablement ajouter le length du code

    vendeur = None
    code = request.GET['code']

    try:
        vendeur = Vendeur.objects.get(code_carte_etudiante=code)
    except Vendeur.DoesNotExist:
        return HttpResponseNotFound()

    reponse = {
               'nom':vendeur.nom,
               'prenom':vendeur.prenom,
               'code_permanent':vendeur.code_permanent,
               'telephone':vendeur.telephone,
               'email':vendeur.email
              }
    
    return HttpResponse(json.dumps(reponse), content_type="application/json")

# Default employee index page
def index_employee(request):
    return render_to_response('encefal/employee/index.html', {},
                              RequestContext(request))

def rapport(request):

  #date= request.GET['nb']
  if request.GET:

    ladate = request.GET['date']
    ladate_dt = dt.strptime(ladate,"%Y-%m-%d")
   

    vendu = Exemplaire.objects.all().filter(facture__date_creation__year=ladate_dt.strftime('%Y'),
                                            facture__date_creation__month=ladate_dt.strftime('%m'),
                                            facture__date_creation__day=ladate_dt.strftime('%d'),)
    ajoute = Exemplaire.objects.all().filter(date_creation__year=ladate_dt.strftime('%Y'),
                                            date_creation__month=ladate_dt.strftime('%m'),
                                            date_creation__day=ladate_dt.strftime('%d'),
                                            )
  else:
    ladate = datetime.date.today()
    vendu = Exemplaire.objects.all().filter(etat="VEND",
                                            facture__date_creation__year=datetime.date.today().year,
                                            facture__date_creation__month=datetime.date.today().month,
                                            facture__date_creation__day=datetime.date.today().day,
                                            )
    ajoute = Exemplaire.objects.all().filter(date_creation__year=datetime.date.today().year,
                                            date_creation__month=datetime.date.today().month,
                                            date_creation__day=datetime.date.today().day,
                                            )

  context = {
    'vendu':vendu,
    'ajoute':ajoute,
    'ladate':ladate,
  }

  return render_to_response('encefal/rapport.html', context)

def rapport_date(request):
#date= request.GET['nb']
  if request.GET:

    ladate = request.GET['date']
    ladate_dt = dt.strptime(ladate,"%Y-%m-%d")
   

    vendu = Exemplaire.objects.all().filter(facture__date_creation__year=ladate_dt.strftime('%Y'),
                                            facture__date_creation__month=ladate_dt.strftime('%m'),
                                            facture__date_creation__day=ladate_dt.strftime('%d'),)
    ajoute = Exemplaire.objects.all().filter(date_creation__year=ladate_dt.strftime('%Y'),
                                            date_creation__month=ladate_dt.strftime('%m'),
                                            date_creation__day=ladate_dt.strftime('%d'),
                                            )
  else:
    ladate = datetime.date.today()
    vendu = Exemplaire.objects.all().filter(etat="VEND",
                                            facture__date_creation__year=datetime.date.today().year,
                                            facture__date_creation__month=datetime.date.today().month,
                                            facture__date_creation__day=datetime.date.today().day,
                                            )
    ajoute = Exemplaire.objects.all().filter(date_creation__year=datetime.date.today().year,
                                            date_creation__month=datetime.date.today().month,
                                            date_creation__day=datetime.date.today().day,
                                            )

  context = {
    'vendu':vendu,
    'ajoute':ajoute,
    'ladate':ladate,
  }

  return render_to_response('encefal/rapport_date.html', context)
