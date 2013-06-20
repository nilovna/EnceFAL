# EnceFAL

EnceFAL est un projet Django, qui vise a faciliter la gestion de foires aux livres usagés

## Installation

<pre>
# cloner le repo
git clone https://github.com/nilovna/EnceFAL.git
cd EnceFAL

# Setter les dependances
python bootstrap.py
bin/buildout

# Modifier les settings pour developpement
cd projet
cp conf.py.edit conf.py
# dans conf.py, editer les configs de la bd locale

# creer la bd locale.
cd ..
bin/django syncdb
# si migration:
# bin/django syncdb --migrate

# Lancer le serveur !
bin/django runserver

# Voilà! le site roule maintenant en localhost.
</pre>
