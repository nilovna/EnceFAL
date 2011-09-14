# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponseRedirect

from ajax_select import make_ajax_form

from project.encefal.models import Vendeur, Session, Livre, Facture, ETAT_LIVRE_CHOICES

class LivreInline(admin.TabularInline):
    model = Livre
    fields = ('isbn', 'titre', 'auteur', 'annee', 'prix', 'etat', )
    extra = 5

class VendeurAdmin(admin.ModelAdmin):
    exclude = ('actif',)
    list_display = ('_vendeur', 'code_permanent', 'telephone', 'email', 
                     'liste_livres',)
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
        import pdb;pdb.set_trace()
        
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
    fields = ('vendeur', 'etat', 'isbn', 'titre', 'auteur', 'annee', 
            'prix',)
    list_display = ('id', '_titre', 'auteur', 'prix', 'annee', 'isbn', 'vendeur', 'etat', 'session',)
    search_fields = ['titre', 'auteur', 'isbn']
    actions = ['vendre',]

    def _titre(self, obj):
        return obj
    _titre.short_description = "Titre"

    def vendre(modeladmin, obj, livres):
        selected = obj.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect(reverse('vendre')+"?ids=%s" % (",".join(selected)))
    vendre.short_description = u'Vendre le(s) livres(s)'
    
    def queryset(self, request):
        qs = self.model._default_manager.get_query_set()
        return qs.filter(etat=ETAT_LIVRE_CHOICES[0][0])

class FactureAdmin(admin.ModelAdmin):
    exclude = ('actif',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(FactureAdmin, self).get_form(request, obj, **kwargs)
        if form.declared_fields.has_key('livres'):
            livres_field = form.declared_fields['livres']
        else:
            livres_field = form.base_fields['livres']
        livres_field.queryset = Livre.objects.filter(etat=ETAT_LIVRE_CHOICES[0][0])
        return form     

    def response_add(self, request, obj, post_url_continue='/../../paiement/'):
        pk_value = obj._get_pk_val()
        return HttpResponseRedirect(reverse('paiement')+"?id=%s" % (pk_value))
    
    def response_change(self, request, obj):
        pk_value = obj._get_pk_val()
        return HttpResponseRedirect(reverse('paiement')+"?id=%s" % (pk_value))

admin.site.register(Vendeur, VendeurAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Livre, LivreAdmin)
admin.site.register(Facture, FactureAdmin)
