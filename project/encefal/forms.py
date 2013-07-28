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

class LivreVendreForm(Form):
    isbn = CharField(required=True, 
                        help_text="Veuillez scanner le code barre du livre",
                        max_length=13)
    titre = CharField(required=True)
    auteur = CharField(required=True)
    prix = DecimalField(required=True)

