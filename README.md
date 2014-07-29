# EnceFAL

EnceFAL est un projet Django, qui vise à faciliter la gestion de foires aux livres usagés

## Installation

```
# cloner le repo
git clone https://github.com/nilovna/EnceFAL.git
cd EnceFAL

# Setter les dépendances
python bootstrap.py -v 2.1.1
bin/buildout

# Modifier les settings pour développement
cd project
cp conf.py.edit conf.py
# dans conf.py, editer les configs de la bd locale

# créer la bd locale.
cd ..
bin/django syncdb --migrate

# Lancer le serveur !
bin/django runserver
```
