# API

Ce programme exécute l'API Backend de l'application ARM qui a pour vocation la gestion des utilisateurs et de leurs scans.

# Dev

On peut déployer l'API en exécutant le programme `bash run/build.sh` sous linux ou `run/build.bat` sous windows. 
Cette commande lance un container contenant python et toutes les dépendences nécéssaire. 
Les informations sensibles sont passées via des variables d'environnement.

Accédez au container via l'extension Dev-container : "Attach to a running container". Le volume créé dans docker-compose persiste les données entre le container et l'hôte de développement (`./app`). 

Lancer les tests depuis le container depuis `/api`.


# Modèle de données

Dans le dossier Maria se trouve le modèle de la base de données Maria DB. 

# Branches

+ master 
+ dev 

# Actions 
Pipeline CI/CD jusqu'au déploiement au push sur la branche master.