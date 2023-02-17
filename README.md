# PyConFR 2023 - "Django Admin comme framework pour développer des outils internes"

> Application de démonstration

Ce dépôt contient un exemple factice d'application métier développée uniquement en utilisant Django Admin.

## Démarrage initial

1. Installer l'environnement virtuel et les dépendances avec `pipenv` :
```bash
pipenv install -d
pipenv shell
```

2. Créer la base de données :
```bash
cp .example.env
python manage.py migrate
```

3. Créer un utilisateur admin :
```bash
python manage.py createsuperuser
```

4. Lancer l'application :
```bash
python manage.py runserver
```
