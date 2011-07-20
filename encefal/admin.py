# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse

from encefal.models import Vendeur, Session, Livre

class VendeurAdmin(admin.ModelAdmin):
   exclude = ('actif',)
   list_display = ('_vendeur', 'code_permanent', 'telephone', 'email', 
                     'liste_livres',)
   search_fields = ['nom', 'prenom']

   def _vendeur(self, obj):
      return obj
   _vendeur.short_description = "Vendeur"

   # Permet de lister tous les livres d'un vendeur
   def liste_livres(self, obj):
      return "<a href='%s?vendeur__id__exact=%s'>Voir les livres\
               </a>" % (reverse('admin:encefal_livre_changelist'), obj.id)
   liste_livres.allow_tags = True 
   liste_livres.short_description = "Liste des livres du vendeur"

class SessionAdmin(admin.ModelAdmin):
   exclude = ('actif',)
   list_display = ('nom', 'date_debut', 'date_fin',)

class LivreAdmin(admin.ModelAdmin):
   # TODO: Le champ session doit être automatiquement mis à la session courante
   #      Vérifier que l'ajout d'un livre soit seulement possible si la date
   #      d'aujourd'hui correspond à une période de la foire aux livre
   fields = ('session', 'vendeur', 'etat', 'isbn', 'titre', 'auteur', 'annee', 
            'prix',)
   list_display = ('_titre', 'auteur', 'prix', 'annee', 'isbn', 'vendeur', 'etat',)
   search_fields = ['titre', 'auteur', 'isbn']

   def _titre(self, obj):
      return obj
   _titre.short_description = "Titre"

   # TODO: Ajouter action, vendre le livre
   #       
   
   

admin.site.register(Vendeur, VendeurAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Livre, LivreAdmin)

