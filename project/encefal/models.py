# -=- encoding: utf-8 -=-
import datetime
from django.db import models

################################################################################
# CONSTANTES (CONSTANTS)
################################################################################ 
HELP_TEXT_FORMAT_DATE = "Le format de la date est JJ-MM-AAAA"

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
    telephone = models.CharField(max_length=255, verbose_name='Téléphone', )
    email = models.EmailField(max_length=255)

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
# LIVRE (BOOK)
################################################################################  
### CHOICES ###
ETAT_LIVRE_CHOICES = (
    ('VENT', 'En vente'),
    ('VEND', 'Vendu'),
    ('PERD', 'Perdu'),
    ('VOLE', 'Volé'),
    ('REND', 'Rendu'),
)

class Livre(Metadata):
    vendeur = models.ForeignKey(Vendeur, db_column='vendeur', related_name='+',)
    session = models.ForeignKey(Session, db_column='session', related_name='+',)
    isbn = models.CharField(max_length=255, blank=True, )
    titre = models.CharField(max_length=255)
    auteur = models.CharField(max_length=255)
    annee = models.PositiveIntegerField(verbose_name='Année', blank=True, )	
    editeur = models.CharField(max_length=255)
    #annee = models.CharField(max_length=255)
    prix = models.DecimalField(max_digits=5, decimal_places=2, help_text="Format 00.00")				
    etat = models.CharField(max_length=4, choices=ETAT_LIVRE_CHOICES, 
                           default='VENT', verbose_name='État', )	

    def save(self, *args, **kwargs):
        session = Session.objects.get(date_debut__lte=datetime.date.today(), 
                                        date_fin__gte=datetime.date.today())
        self.session = session
        super(Livre, self).save(*args, **kwargs)

    def __unicode__(self):
      return '[%s] %s, %s' % (self.id, self.titre, self.auteur)

################################################################################
# FACTURE (INVOICE)
################################################################################  
class Facture(Metadata):
    livres = models.ManyToManyField(Livre, db_column='livre', related_name='livres',)

    def __unicode__(self):
      return 'Facture #%s' % (self.id)
