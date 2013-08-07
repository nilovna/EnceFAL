# -*- encoding: utf-8 -*-
from django.forms import ModelForm,Form
from django.forms import IntegerField, CharField, DecimalField
from project.encefal.models import Exemplaire,Vendeur

class ExemplaireForm(ModelForm):
    class Meta:
        model = Exemplaire

class VendeurForm(ModelForm):
    class Meta:
        model = Vendeur
        exclude = ['actif']
        fields = ['code_carte_etudiante', 
                  'code_permanent', 
                  'prenom', 
                  'nom' , 
                  'email']
    class Media:
        js = {
                all: ('js/vente.js',)
                }

class LivreVendreForm(ModelForm):
    exclude = ( 'actif', 'livre', 'etat',)

    isbn = CharField(required=True, 
                        help_text="Scannez le code barre du livre",
                        label="ISBN",
                        max_length=13)

    titre = CharField(required=True, 
                      label="Titre",
                      help_text="Titre")

    auteur = CharField(required=True, 
                       label="Auteur",
                       help_text="Auteur")
    
    prix = DecimalField(required=True, 
                        label="Prix demandé",
                        help_text="Prix")
    class Meta:
        model = Exemplaire

