# Installation

python 3.11
requirements.txt

# Branches

+ master 
+ dev 
+ test (feature unit test)

# Dossiers

## Checkpoint dans gitignore 

télécharger les modèles yolov8x et yolov8x 
https://github.com/ultralytics/ultralytics/tree/main
On peut télécharger les checkpoints pour COCO ou openimageV7, détection ou segmentation. 

## Data
### Sample

Dans git. Il y a quelques exemples de données pour faire des tests.

### Dataset dans gitignore

On peut ajouter d'autre dataset dans gitignore pour l'entrainement des modèles.

## Modeles

### Modele 1 (Projet E1)

Meilleur modèle à ce jour : yolov8n_custom201223_train9.pt
yolov8 fine-tuné avec un dataset custom de openimagev7 et SKU110k
Modèle de détection d'objet utilisé pour la création automatique du dataset.

### Modele 2 

Modèle qui servira à associer une image à un code barre. 

## Backend

Script d'anotation automatique.

### API

Mise en place de l'API sur un VPS.
Cette API sert à communiquer avec les bases de données MongoDB pour la gestion des datasets et MariaDB pour analyse de données.
L'API est dans un conteneur Docker. Placer les fichers backend/api/ sur un hôte et lancer "```docker compose up```"/"```docker-compose up --force-recreate --build```".
Penser à configurer uvicorn pour la production dans le DockerFile. 

Pour le dev, lancer le build + run du container et accéder au container via l'extension Dev-container : "Attach to a running container". Le volume créé dans docker-compose persiste les données entre le container et l'hôte de développement (```./app```). 

Lancer les tests depuis le container depuis ```/api```.

### MariaDB

Initialisation du modèle de données de la base MariaDB. 

### Mongodb 

Informations relatives aux à cette bases de données et aux datasets.  

## Trackers

Configuration des trackers utilisés avec YoloV8