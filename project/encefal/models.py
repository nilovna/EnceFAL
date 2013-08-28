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

    def nb_livres(self):
        return self.exemplaires.count()
    nb_livres.short_description = 'Nombre de livres'


class Reception(Vendeur):
    class Meta:
        proxy = True
        verbose_name = "Vendeur"

    def __unicode__(self):
        return ("Reception de livres de " + self.nom + ', ' + self.prenom)

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

    @staticmethod
    def current_session():
        try:
            reponse = Session.objects.get(date_debut__lte=datetime.date.today(),
                                       date_fin__gte=datetime.date.today())
        except Session.DoesNotExist:
            reponse = None

        return reponse



################################################################################
# FACTURE (INVOICE)
################################################################################
class Facture(Metadata):
    employe = models.ForeignKey(User, db_column='employe',
                                related_name='factures',blank=True)
    session = models.ForeignKey(Session, db_column='session',
                                related_name='factures',blank=True)

    def __unicode__(self):
      return 'Facture #%s' % (self.id)

    def nb_livres(self):
        return self.exemplaires.count()
    nb_livres.short_description = 'Nombre de livres'


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

    def exemplaires_en_vente(self):
        return [e for e in self.exemplaires.all() if e.etat == 'VENT']
    exemplaires_en_vente.short_description = 'Exemplaires en vente'

    def nb_exemplaires_en_vente(self):
        return len(self.exemplaires_en_vente())
    nb_exemplaires_en_vente.short_description = 'Nombre d\'exemplaires en vente'

    def prix_moyen(self):
        exemplaires = self.exemplaires_en_vente()
        return (sum([e.prix for e in exemplaires]) / len(exemplaires))

    def save(self, *args, **kwargs):

        if not self.edition:
            self.edition = 1

        super(Livre, self).save(*args, **kwargs)

    def __unicode__(self):
      return '%s [%s]' % (self.titre, self.auteur)


class Vente(Facture):
    class Meta:
        proxy = True

    def __unicode__(self):
        return ""

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

    def titre(self):
        return (self.livre.titre)
    titre.short_description = 'Titre'

    def save(self,*args,**kwargs):

        code_vendeur = self.vendeur.code_carte_etudiante
        pk_vendeur_temp = self.vendeur.id
        vendeur = None

        try:
            self.vendeur = (
                            Vendeur.objects.all().
                            exclude(pk=pk_vendeur_temp).
                            get(code_carte_etudiante=code_vendeur)
                           )
        except Vendeur.DoesNotExist:
            pass

        super(Exemplaire,self).save(*args,**kwargs)
