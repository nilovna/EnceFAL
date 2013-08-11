# -=- encoding: utf-8 -=-
import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import ValidationError
import urllib, json

################################################################################
# CONSTANTES (CONSTANTS)
################################################################################
HELP_TEXT_FORMAT_DATE = "Le format de la date est JJ-MM-AAAA"
#Ajouter une KEY propre a Encefal. On doit creer un compte sur isbndb
ISBN_DB_BASE_QUERY = "http://isbndb.com/api/v2/json/{0}/book/{1}"

################################################################################
# ABSTRAIT (ABSTRACT)
################################################################################
class Metadata(models.Model):
    """
    actif == False : objet réputé supprimé.
    """
    actif = models.BooleanField(default=True)
    date_creation = models.DateField(auto_now_add=True,
                                    help_text=HELP_TEXT_FORMAT_DATE, )

    class Meta:
        abstract = True

################################################################################
# VENDEUR (SELLER)
################################################################################
class Vendeur(Metadata):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255, verbose_name='Prénom', )
    code_permanent = models.CharField(max_length=12, )
    code_carte_etudiante = models.IntegerField(null=False, blank=False,
                                       verbose_name="Code de la carte étudiante",
                                       help_text="Scannez la carte étudiante")
    telephone = models.CharField(max_length=255, verbose_name='Téléphone',
                                 blank=True)
    email = models.EmailField(max_length=255, blank=True)

    def __unicode__(self):
        return '%s, %s' % (self.nom, self.prenom)

class Reception(Vendeur):
    class Meta:
        proxy = True

    def __unicode__(self):
        return ("Reception de livres de " + 
                self.nom + ', ' + 
                self.prenom)

class Vente(User):
    class Meta:
        proxy = True

    def __unicode__(self):
        return ("Vente par" + 
                self.last_name + ', ' + 
                self.first_name)

################################################################################
# SESSION (SEMESTER)
################################################################################
class Session(Metadata):
    nom = models.CharField(max_length=255, unique=True, )
    date_debut = models.DateField(verbose_name="Date début",
                             help_text=HELP_TEXT_FORMAT_DATE,)
    date_fin = models.DateField(help_text=HELP_TEXT_FORMAT_DATE,)

    def __unicode__(self):
        return '%s' % (self.nom)

################################################################################
# FACTURE (INVOICE)
################################################################################
class Facture(Metadata):
    employe = models.ForeignKey(User, db_column='employe',
                                related_name='factures',)
    session = models.ForeignKey(Session, db_column='session',
                                related_name='factures',)

    def __unicode__(self):
      return 'Facture #%s' % (self.id)

################################################################################
# LIVRE (BOOK)
################################################################################
class Livre(Metadata):
    vendeur = models.ManyToManyField(Vendeur, db_column='vendeur',
                                     related_name='livres', through='Exemplaire')
    isbn = models.CharField(max_length=13, blank=True, null=False, unique=True)
    titre = models.CharField(max_length=255, blank=True, )
    auteur = models.CharField(max_length=255, blank=True)
    edition = models.PositiveIntegerField(verbose_name='Édition', default=1,
                                          blank=True, null=False,)

    def save(self, *args, **kwargs):

        if not self.edition:
            self.edition = 1

        super(Livre, self).save(*args, **kwargs)

    def __unicode__(self):
      return '%s [%s]' % (self.titre, self.auteur)


################################################################################
# EXEMPLAIRE (COPY)
################################################################################
### CHOICES ###
ETAT_LIVRE_CHOICES = (
    ('VENT', 'En vente'),
    ('VEND', 'Vendu'),
    ('PERD', 'Perdu'),
    ('VOLE', 'Volé'),
    ('REND', 'Rendu'),
)
class Exemplaire(Metadata):
    facture = models.ForeignKey(Facture, db_column='facture',
                                related_name='exemplaires', null=True,
                                blank=True)
    livre = models.ForeignKey(Livre, db_column='livre',
                              related_name='exemplaires',)
    vendeur = models.ForeignKey(Vendeur, db_column='vendeur',
                                related_name='exemplaires',)
    etat = models.CharField(max_length=4, choices=ETAT_LIVRE_CHOICES,
                            default='VENT', verbose_name='État', )
    prix = models.DecimalField(max_digits=5, decimal_places=2,
                               help_text="Format 00.00")

    def __unicode__(self):
        return self.livre.__unicode__()

