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

admin.site.register(Vendeur)
admin.site.register(Session, SessionAdmin)
admin.site.register(Livre, LivreAdmin)
admin.site.register(Facture)
admin.site.register(Exemplaire)
