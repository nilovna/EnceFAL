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
    telephone = models.CharField(max_length=255, verbose_name='Téléphone',
                                 blank=True)
    email = models.EmailField(max_length=255, blank=True)

    def __unicode__(self):
        return '%s, %s [%s]' % (self.nom, self.prenom, self.id)

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

    def clean(self, *args, **kwargs):

        #TODO: verifier le isbn avec un regex

        if self.pk is None:
            if self.isbn and not self.titre:
                if not self.rechercher_infos():
                    raise ValidationError('Impossible de populer les infos \
                                          avec ce isbn.\n \
                                          Veuillez les saisir manuellement.')

        super(Livre, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):

        if not self.edition:
            self.edition = 1

        session = Session.objects.get(date_debut__lte=datetime.date.today(),
                                      date_fin__gte=datetime.date.today())
        self.session = session
        super(Livre, self).save(*args, **kwargs)

    def rechercher_infos(self):

        trouvees = False

        query = ISBN_DB_BASE_QUERY.format(settings.ISBNDB_API_KEY, self.isbn)
        reponse = json.load(urllib.urlopen(query))
        if  'error' in reponse:
            trouvees = False
        else:
            reponse = reponse['data'][0]
            self.titre = reponse['title']
            self.auteur = reponse['author_data'][0]['name']
            #Impossible d'avoir l'annee avec isbndb
            #self.annee = 2013
            trouvees = True

        return trouvees

    def __unicode__(self):
      return '%s, %s [%s]' % (self.id, self.titre, self.auteur)


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

