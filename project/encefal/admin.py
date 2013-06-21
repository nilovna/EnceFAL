# -*- encoding: utf-8 -*-
import datetime
from django.contrib import admin
from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponseRedirect

from project.encefal.models import Vendeur, Session, Livre, Facture, ETAT_LIVRE_CHOICES, Exemplaire

class LivreInline(admin.TabularInline):
    model = Livre
    fields = ('isbn', 'titre', 'auteur')
    extra = 15

class VendeurAdmin(admin.ModelAdmin):
    exclude = ('actif',)
    list_display = ('_vendeur', 'code_permanent', 'telephone', 'email', 
                     'liste_livres', 'date_creation', )
    search_fields = ['nom', 'prenom']
    inlines = [LivreInline, ]
    def _vendeur(self, obj):
        return obj
    _vendeur.short_description = "Vendeur"

    # Permet de lister tous les livres d'un vendeur
    def liste_livres(self, obj):
        return "<a href='%s?id=%s'>Voir les livres\
               </a>" % (reverse('liste_livres'), obj.id)
    liste_livres.allow_tags = True 
    liste_livres.short_description = "Liste des livres du vendeur"

    def response_add(self, request, obj, post_url_continue='/../../liste_livres/'):
        pk_value = obj._get_pk_val()
        return HttpResponseRedirect(reverse('liste_livres')+"?id=%s" % (pk_value))
    
    def response_change(self, request, obj):
        pk_value = obj._get_pk_val()
        return HttpResponseRedirect(reverse('liste_livres')+"?id=%s" % (pk_value))

class SessionAdmin(admin.ModelAdmin):
    exclude = ('actif',)
    list_display = ('nom', 'date_debut', 'date_fin',)

class LivreAdmin(admin.ModelAdmin):
    # TODO: Le champ session doit être automatiquement mis à la session courante
    #      Vérifier que l'ajout d'un livre soit seulement possible si la date
    #      d'aujourd'hui correspond à une période de la foire aux livre
    fields = ('isbn', 'titre', 'auteur', 'edition')
    list_display = ('isbn', 'titre', 'auteur', 'edition')
    search_fields = ['titre', 'auteur', 'isbn']

admin.site.register(Vendeur, VendeurAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Livre, LivreAdmin)
admin.site.register(Facture)
admin.site.register(Exemplaire)
