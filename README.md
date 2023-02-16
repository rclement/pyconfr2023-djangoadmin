# PyConFR 2023 - "Django Admin comme framework pour développer des outils internes"

> Application de démonstration

Ce dépôt contient un exemple factice d'application métier développée uniquement en utilisant Django Admin.

## Démarrage

Installer l'environnement virtuel et les dépendances avec `pipenv` :

```bash
pipenv install -d
pipenv shell
```

Créer la base de données et lancer l'application :

```bash
cp .example.env
python manage.py migrate
python manage.py runserver
```
