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

class LivreVendreForm(Form):
    isbn = IntegerField(required=True, 
                        help_text="Veuillez scanner le code barre du livre")
    titre = CharField(required=True)
    auteur = CharField(required=True)
    prix = DecimalField(required=True)

    def is_valid():
        return False
