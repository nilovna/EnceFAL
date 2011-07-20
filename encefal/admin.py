# -*- encoding: utf-8 -*-
from django.contrib import admin
from encefal.models import Vendeur, Session, Livre

class VendeurAdmin(admin.ModelAdmin):
   exclude = ('actif',)
   list_display = ('_vendeur', 'code_permanent', 'telephone', 'email', )

   def _vendeur(self, obj):
      return obj
   _vendeur.short_description = "Vendeur"

   # TODO: Voir la liste de tous les livres du vendeur
   

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

   def _titre(self, obj):
      return obj
   _titre.short_description = "Titre"

   # TODO: Ajouter action, vendre le livre
   #       
   
   

admin.site.register(Vendeur, VendeurAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Livre, LivreAdmin)

