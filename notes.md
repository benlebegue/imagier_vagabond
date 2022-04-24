# Utilisation pour Benjamin

## Version courte

Utiliser iTerm, et lancer ces 3 commandes dans un premier onglet:

```
cd ~/Documents/Imagiervagabond/imagiervagabond.fr
source venv/bin/activate
python ./manage.py runserver localhost:8000
```

Ouvrir un deuxième onglet, et lancer:

```
cd ~/Documents/Imagiervagabond/imagiervagabond.fr/public
python -m http.server 8001
```

Et ouvrir le site à http://localhost:8000

## Vérifier que la base de données tourne

```
brew services
```

Si besoin de la relancer:

```
brew services stop mariadb
brew services start mariadb
```

## Réinstaller les dépendences Python

(Attention, bien avoir activé virtualenv avant!)

```
pip install -r requirements.txt
```
