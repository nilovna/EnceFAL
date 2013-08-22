# -*- encoding: utf-8 -*-
import datetime

from django.contrib import admin
from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponseRedirect

from project.encefal.forms import LivreVendreForm, VendeurForm, LivreVenteForm
from project.encefal.models import (
                                    Vendeur, Session,
                                    Livre, Facture,
                                    ETAT_LIVRE_CHOICES,
                                    Exemplaire, Reception,
                                    Vente, Facture
                                   )

class LivreFormInline(admin.TabularInline):
    exclude = ['facture', 'actif', 'etat', 'livre']
    model = Exemplaire
    form = LivreVendreForm
    fields = ['isbn', 'titre', 'auteur', 'prix']
    extra = 1

class LivreVenteFormInline(admin.TabularInline):
 
    exclude = [ 'actif', 'etat', 'livre']
    model = Exemplaire
    form = LivreVenteForm
    fields = ['identifiant','isbn', 'titre', 'auteur', 'prix']
    #readonly_fields = ('isbn','titre','auteur', 'prix')
    extra = 15

class SessionAdmin(admin.ModelAdmin):
    exclude = ('actif',)
    list_display = ('nom', 'date_debut', 'date_fin',)

class ReceptionAdmin(admin.ModelAdmin):
    model = Reception
    exclude = ('actif',)
    inlines = [ LivreFormInline, ]

class VenteAdmin(admin.ModelAdmin):

    def __init__(self, *args, **kwargs):
        super(VenteAdmin, self).__init__(*args, **kwargs)
        self.model.session = Session.current_session()

    def get_form(self, request, obj=None, **kwargs):
        form = super(VenteAdmin, self).get_form(request, obj, **kwargs)
        self.model.employe = request.user
        return form

    model = Facture
    readonly_fields = ('employe','session',)
    exclude = ('actif',)
    inlines = [ LivreVenteFormInline, ]

class LivreAdmin(admin.ModelAdmin):
    fields = ('isbn', 'titre', 'auteur', 'edition')
    list_display = ('isbn', 'titre', 'auteur', 'edition')
    search_fields = ['titre', 'auteur', 'isbn']

class ExemplaireAdmin(admin.ModelAdmin):
    list_display = ('vendeur', 'etat', 'pk',)

admin.site.register(Vendeur)
admin.site.register(Reception, ReceptionAdmin)
admin.site.register(Vente, VenteAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Livre, LivreAdmin)
admin.site.register(Facture)
admin.site.register(Exemplaire, ExemplaireAdmin)
