# API de Questionnaires avec FastAPI
## contexte 
# une entreprise qui crée des questionnaires via une application pour Smartphone ou pour navigateur Web. Pour simplifier l'architecture de ces différents produits, l'entreprise veut mettre en place une API. Celle-ci a pour but d'interroger une base de données pour retourner une série de questions.


## Choix d'Architecture

1. **FastAPI** : Choisi pour sa performance et sa simplicité d'utilisation. Il permet de créer des APIs rapidement et avec une documentation automatique.
2. **Authentification Basique** : Utilisée pour la simplicité, avec un dictionnaire en mémoire pour stocker les utilisateurs. Pour une application réelle, il faudrait envisager une méthode plus sécurisée.
3. **Pandas** : Utilisé pour manipuler les données de questions, car il offre des fonctionnalités puissantes pour le filtrage et la manipulation des données.

## Instructions pour Exécuter le Projet

1. **Installer les dépendances** :
    ```pip install -r requirements.txt
    ```

2. **Télécharger le fichier CSV** :
    ```curl wget https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_fr/questions.csv
    ```

3. **Lancer l'application FastAPI** :
    ```sh   uvicorn main:app --reload
    ```

4. **Tester les endpoints** :
    - Utiliser les requêtes définies dans le fichier `test_requests.http` avec  [Postman](https://www.postman.com/)  on peut aussi tester via la plateforme HTTPs
