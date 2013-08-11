# -*- encoding: utf-8 -*-
from django.forms import ModelForm,Form
from django.forms import IntegerField, CharField, DecimalField
from project.encefal.models import Exemplaire,Vendeur,Livre,ETAT_LIVRE_CHOICES

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

    def clean(self):
        cleaned_data = super(LivreVendreForm, self).clean()
        
        livre, created = Livre.objects.get_or_create(isbn=cleaned_data.get('isbn'))
        if created:
            livre.auteur = cleaned_data.get('auteur')
            livre.titre = cleaned_data.get('titre')

        livre.save()
        self.instance.livre = livre
        
        return cleaned_data

    class Meta:
        model = Exemplaire

