# -=- encoding: utf-8 -=-
from django.db import models

################################################################################
# CONSTANTES (CONSTANTS)
################################################################################ 
HELP_TEXT_FORMAT_DATE = "Le format de la date est AAAA-MM-JJ"

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
)
      
class Livre(Metadata):
   vendeur = models.ForeignKey(Vendeur, db_column='vendeur', related_name='+',)
   session = models.ForeignKey(Session, db_column='session', related_name='+',)
   isbn = models.CharField(max_length=255)
   titre = models.CharField(max_length=255)
   auteur = models.CharField(max_length=255)
   annee = models.PositiveIntegerField(verbose_name='Année', blank=True, )	
   prix = models.DecimalField(max_digits=5, decimal_places=2, )				
   etat = models.CharField(max_length=4, choices=ETAT_LIVRE_CHOICES, 
                           default='VENT', verbose_name='État', )	

   def __unicode__(self):
      return '%s - %s [%s]' % (self.titre, self.auteur, self.id)    	      								 
