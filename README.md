# Projet Démineur

## Description
Ce projet consiste à créer un jeu de démineur connecté, contrôlé via une interface web interactive. Le système intègre des capteurs physiques pour interagir avec le plateau de jeu, poser des marques, et déminer.

### Fonctionnalités principales
- Interface web pour jouer et suivre les scores.
- Plateau de démineur personnalisable.
- Gestion et interaction avec des capteurs physiques pour enrichir l'expérience de jeu.
- Suivi de l'évolution des joueurs via des graphiques dynamiques.

## Structure des fichiers

### Backend
- **server.py** :
  - Basé sur FastAPI, ce fichier contient l'implémentation du backend.
  - Gestion des requêtes pour les capteurs physiques.
  - Communication avec l'interface web (envoi/réception des données du jeu).

- **create_plateau_demineur.py** :
  - Script pour générer les champs de mines. (avec difficulté différente)

### Frontend
- **Fichiers JavaScript :**
  - Affichage du champ de mines.
  - Barre de navigation et menus déroulants.
  - Interface pour créer un champ de mines personnalisé.

- **Fichiers HTML :**
  - Base du site web.
  - Intégration des éléments visuels et scripts JavaScript.
