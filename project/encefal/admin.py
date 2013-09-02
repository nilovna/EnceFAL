# -*- encoding: utf-8 -*-
import datetime
import pdb

from django.contrib import admin
from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponseRedirect

from project.encefal.forms import (
                                   ExemplaireVenteForm, 
                                   ExemplaireReceptionForm, 
                                  )
from project.encefal.models import (
                                    Vendeur, Session,
                                    Livre, Facture,
                                    ETAT_LIVRE_CHOICES,
                                    Exemplaire, Reception,
                                    Vente, Facture
                                   )



class ExemplaireReceptionInline(admin.TabularInline):

    exclude = ['facture', 'actif', 'etat', 'livre']
    model = Exemplaire
    form = ExemplaireReceptionForm
    fields = ['isbn', 'titre', 'auteur', 'prix']
    extra = 5

class ExemplaireVenteInline(admin.TabularInline):

    exclude = [ 'actif', 'etat', 'livre']
    model = Exemplaire
    form = ExemplaireVenteForm
    fields = ['identifiant','isbn', 'titre', 'auteur', 'prix']
    extra = 15

class SessionAdmin(admin.ModelAdmin):
    exclude = ('actif',)
    list_display = ('nom', 'date_debut', 'date_fin',)

class ReceptionAdmin(admin.ModelAdmin):
    model = Reception
    exclude = ('actif',)
    fields = [
              'code_permanent', 
              'prenom', 
              'nom' , 
              'email',
              'telephone'
             ]
    inlines = [ ExemplaireReceptionInline, ]
    list_display = ('date_creation', 'nom', 'prenom',
                    'nb_livres', 'code_permanent')

    def save_model(self, request, obj, form, change):
        #ne save pas le modele si le meme vendeur existe deja!
        try:
            Vendeur.objects.get(code_permanent=obj.code_permanent)
        except Vendeur.DoesNotExist:
            obj.save()
        return

    #TODO: utiliser url reverser
    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect('/employee/')

    def has_change_permission(self, request, obj=None):
        return obj is None or False

def annuler_vente(modeladmin, request, queryset):
    for vente in queryset.all():
        exemplaires = vente.exemplaires
        for exemplaire in exemplaires.all():
            exemplaire.etat = 'VENT'
            exemplaire.facture = None
            exemplaire.save()
    queryset.delete()
    return HttpResponseRedirect('/employee/')
annuler_vente.short_description = "Annuler la ou les vente(s) selectionnée(s)"

class VenteAdmin(admin.ModelAdmin):

    def __init__(self, *args, **kwargs):
        super(VenteAdmin, self).__init__(*args, **kwargs)
        self.model.session = Session.current_session()

    def get_form(self, request, obj=None, **kwargs):
        form = super(VenteAdmin, self).get_form(request, obj, **kwargs)
        self.model.employe = request.user
        return form

    def save_model(self, request, obj, form, change):
        obj.employe_id = self.model.employe.id
        obj.session_id = self.model.session.id
        obj.save()

    #TODO: utiliser url reverser admin_index ??
    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect('/employee/')

    def has_change_permission(self, request, obj=None):
        return obj is None or False

    def has_delete_permission(self, request, obj=None):
        return obj is not None or False

    def get_actions(self, request):
        actions = { 'annuler_vente':(annuler_vente, 'annuler_vente', annuler_vente.short_description) }
        return actions

    model = Facture
    readonly_fields = ('employe','session',)
    fields = ('employe', 'session')
    list_display = ( 'date_creation', 'employe', 'session', 'nb_livres', 'prix_total',)
    exclude = ('actif',)
    actions = [ annuler_vente ]
    inlines = [ ExemplaireVenteInline, ]

class LivreAdmin(admin.ModelAdmin):
    fields = ('isbn', 'titre', 'auteur', 'edition')
    list_display = ('isbn', 'titre', 'auteur', 'edition')
    search_fields = ['titre', 'auteur', 'isbn']

class ExemplaireAdmin(admin.ModelAdmin):
    list_display = ('id','titre','vendeur','etat','prix','date_creation', 'date_modification', 'facture' )
    order_by = ('date_creation', 'date_modification')
    search_fields = ('livre__isbn','livre__titre','id')

class FactureAdmin(admin.ModelAdmin):
    list_display = ('date_creation', 'employe', 'session', 'nb_livres',)

class VendeurAdmin(admin.ModelAdmin):
    list_display = ('date_creation', 'nom', 'prenom', 'nb_livres', 'code_permanent')
    exclude = ['actif']
    fields = [
              'code_permanent', 
              'prenom', 
              'nom' , 
              'email'
             ]

admin.site.register(Vendeur, VendeurAdmin)
admin.site.register(Reception, ReceptionAdmin)
admin.site.register(Vente, VenteAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Livre, LivreAdmin)
admin.site.register(Facture, FactureAdmin)
admin.site.register(Exemplaire, ExemplaireAdmin)
