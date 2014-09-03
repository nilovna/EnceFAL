# -=- encoding: utf-8 -=-
import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import ValidationError
import urllib, json

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

################################################################################
# CONSTANTES (CONSTANTS)
################################################################################
HELP_TEXT_FORMAT_DATE = "Le format de la date est JJ/MM/AAAA"
#Ajouter une KEY propre a Encefal. On doit creer un compte sur isbndb
ISBN_DB_BASE_QUERY = "http://isbndb.com/api/v2/json/{0}/book/{1}"
COOP_UQAM_BASE_QUERY = "http://www.coopuqam.com/resultat-recherche.html?MotCle={0}"

################################################################################
# ABSTRAIT (ABSTRACT)
################################################################################
class Metadata(models.Model):
    """
    actif == False : objet réputé supprimé.
    """
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True,
                                    help_text=HELP_TEXT_FORMAT_DATE, )
    date_modification = models.DateTimeField(auto_now=True,
                                    help_text=HELP_TEXT_FORMAT_DATE, )

    class Meta:
        abstract = True

################################################################################
# VENDEUR (SELLER)
################################################################################
class Vendeur(Metadata):
    class Meta:
        verbose_name = "Vendeur (Vrai)"
        verbose_name_plural = "Vendeurs (Vrai)"

    # En attendant les scanners, ce champ est inutile.
    #code_carte_etudiante = models.IntegerField(null=False, blank=False,
                                       #verbose_name="Code carte étudiante",
                                       #help_text="Scannez la carte étudiante")
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255, verbose_name='Prénom', )
    code_permanent = models.CharField(max_length=12)
    email = models.EmailField(max_length=255, blank=False)
    telephone = models.CharField(max_length=255, verbose_name='Téléphone',
                                 blank=True)

    def __unicode__(self):
        return '%s, %s' % (self.nom, self.prenom)

    def nb_livres(self):
        return self.exemplaires.count()
    nb_livres.short_description = 'Nombre de livres'

    def envoyer_recu(self):
        '''
        lorsque le vendeur apporte des livres, on envoie le contrat par email.
        '''
        plaintext = get_template('encefal/vendeur/initial.txt')
        htmly     = get_template('encefal/vendeur/initial.html')

        d = Context({ 'vendeur': self })

        subject, from_email, to = 'contrat', 'aess@aessuqam.org', self.email
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to],)
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=True)

class Reception(Vendeur):
    class Meta:
        proxy = True
        verbose_name = "Vendeur"
        verbose_name_plural = "Vendeurs"

    def __unicode__(self):
        return ("Reception de livres de " + self.nom + ', ' + self.prenom)

################################################################################
# SESSION (SEMESTER)
################################################################################
class Session(Metadata):
    nom = models.CharField(max_length=255, unique=True, )
    date_debut = models.DateField(verbose_name="Date début",
                             help_text=HELP_TEXT_FORMAT_DATE, null=True, blank=True)
    date_fin = models.DateField(help_text=HELP_TEXT_FORMAT_DATE, null=True, blank=True)

    def __unicode__(self):
        return '%s' % (self.nom)

    @staticmethod
    def next_session():
        reponse = Session.objects.filter(date_debut__gte=datetime.date.today())
        if not reponse.count():
            return None
        else:
            return reponse.order_by('date_debut')[0]

    @staticmethod
    def current_session():
        try:
            reponse = Session.objects.get(date_debut__lte=datetime.date.today(),
                                       date_fin__gte=datetime.date.today())
        except Session.DoesNotExist:
            reponse = None

        return reponse

    @staticmethod
    def session_null():
        return Session.objects.get(nom="/dev/null")



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

    def prix_total(self):
        return sum([e.prix for e in self.exemplaires.all()]) or 0
    prix_total.short_description = 'Prix total de la facture'


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
    ('REMB', 'Remboursé'),
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
    prix = models.IntegerField(help_text="Le prix doit être un entier!")

    def __unicode__(self):
        return self.livre.__unicode__()

    def titre(self):
        return (self.livre.titre)
    titre.short_description = 'Titre'

    def code_permanent_vendeur(self):
        return (self.vendeur.code_permanent)
    code_permanent_vendeur.short_description = 'Vendeur'

    def save(self,*args,**kwargs):

        code_permanent = self.vendeur.code_permanent
        pk_vendeur_temp = self.vendeur.id
        vendeur = None

        try:
            self.vendeur = (
                            Vendeur.objects.all().
                            exclude(pk=pk_vendeur_temp).
                            get(code_permanent=code_permanent)
                           )
        except Vendeur.DoesNotExist:
            pass

        super(Exemplaire,self).save(*args,**kwargs)
