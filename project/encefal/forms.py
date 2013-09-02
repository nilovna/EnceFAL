# -*- encoding: utf-8 -*-
from django.forms import ModelForm,Form, TextInput
from django.forms import IntegerField, CharField, DecimalField
from project.encefal.models import Exemplaire,Vendeur,Livre,ETAT_LIVRE_CHOICES

class IsbnTextInput(TextInput):

    def __init__(self, attrs=None):
        if attrs:
            attrs['onchange'] = 'get_isbn(event);'
        else:
            attrs = {'onchange':'get_isbn(event);'}

        super(TextInput, self).__init__(attrs) 

class IdentifiantTextInput(TextInput):

    def __init__(self, attrs=None):
        if attrs:
            attrs['onchange'] = 'get_exemplaire(event);'
        else:
            attrs = {'onchange':'get_exemplaire(event);'}

        super(TextInput, self).__init__(attrs) 

class ExemplaireReceptionForm(ModelForm):
    exclude = ( 'actif', 'livre', 'etat',)

    isbn = CharField(
                     required=True, 
                     help_text="Scannez le code barre du livre",
                     label="ISBN",
                     widget=IsbnTextInput,
                     max_length=13
                    )

    titre = CharField(required=True, 
                      label="Titre",
                      help_text="Titre")

    auteur = CharField(required=True, 
                       label="Auteur",
                       help_text="Auteur")
    
    def clean(self):
        cleaned_data = super(ExemplaireReceptionForm, self).clean()
        
        livre, created = Livre.objects.get_or_create(isbn=cleaned_data.get('isbn'))
        if created:
            livre.auteur = cleaned_data.get('auteur')
            livre.titre = cleaned_data.get('titre')

        livre.save()
        self.instance.livre = livre
        
        return cleaned_data

    class Meta:
        model = Exemplaire

class ExemplaireVenteForm(ModelForm):

    exclude = ( 'actif', 'livre', 'etat',)

    isbn = CharField(required=True, 
                        help_text="Scannez le code barre du livre",
                        label="ISBN",
                        max_length=13)

    titre = CharField(required=True, 
                      label="Titre",
                      help_text="Titre")

    identifiant = IntegerField(required=True, 
                      label="Identifiant",
                      help_text="Identifiant",
                      widget=IdentifiantTextInput)

    auteur = CharField(required=True, 
                       label="Auteur",
                       help_text="Auteur")
    
    prix = DecimalField(required=True, 
                        label="Prix demandé",
                        help_text="Prix")

    def clean(self):
        cleaned_data = super(ExemplaireVenteForm, self).clean()
        self.instance = Exemplaire.objects.get(pk=cleaned_data['identifiant'])
        self.instance.etat = 'VEND'
        self.instance.save()
        return cleaned_data

    class Meta:
        model = Exemplaire

