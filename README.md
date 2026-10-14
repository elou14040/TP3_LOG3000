Calculatrice Web (Flask)
Application web simple de calculatrice, construite avec Python et la bibliothèque Flask. Ce dépôt centralise le code, la documentation et le processus de collaboration de l'équipe.

Equipe
Nous sommes l'équipe 17 avec comme membre:
Ibrahima Gueye 2161023
Mounder Chaourar 2301906

Description
L'application offre une interface web permettant d'effectuer des opérations arithmétiques de base. Le frontend (HTML/CSS) envoie les calculs au backend Flask, qui applique la logique de calcul et retourne le résultat.

Objectif
Ce projet vise à fournir une calculatrice web simple, fiable et maintenable. Les objectifs de ce dépôt sont :
Centraliser le code de la calculatrice (frontend et backend) dans un dépôt GitHub partagé par toute l'équipe.
Mettre en place de bonnes pratiques de gestion de versions : branches, pull requests, révisions de code.
Documenter le dépôt et chaque composant de la base de code (rôle, fonctionnement, utilisation).
Corriger les bogues présents dans la logique du backend et ajouter des tests pour garantir la fiabilité de l'application.
Automatiser la vérification du code au moyen d'un pipeline d'intégration continue documenté.

Composants
Frontend - interface	fichier HTML	Affiche la calculatrice et envoie les opérations au serveur
Frontend - style	fichier CSS	Gère l'apparence de l'interface
Backend - serveur	fichier(s) Python	Exécute le serveur Flask et définit les routes
Backend - logique	fichier(s) Python	Effectue les calculs et valide les entrées

Prérequis
Un compte GitHub
Git
Python 3.9 ou plus récent
pip

Installation
bash
# 1. Cloner le dépôt
git clone https://github.com/<organisation-ou-utilisateur>/<nom-du-depot>.git
cd <nom-du-depot>

# 2. (Recommandé) Créer un environnement virtuel
python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt
