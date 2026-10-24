# Calculatrice Web (Flask)

Application web simple de calculatrice, construite avec Python et la bibliothèque Flask.
Ce dépôt centralise le code, la documentation et le processus de collaboration de l'équipe.

## Équipe

**Équipe n° 17** — LOG3000

| Membre           | Matricule |
|------------------|-----------|
| Ibrahima Gueye   | 2161023   |
| Mounder Chaourar | 2301906   |

## Description

L'application offre une interface web permettant d'effectuer des opérations arithmétiques
de base (addition, soustraction, multiplication, division). Le frontend (HTML/CSS) envoie
l'expression saisie au backend Flask, qui applique la logique de calcul et retourne le résultat.

## Objectif

Fournir une calculatrice web simple, fiable et maintenable. Plus précisément, ce dépôt vise à :

- Centraliser le code de la calculatrice (frontend et backend) dans un dépôt GitHub partagé par l'équipe.
- Mettre en place de bonnes pratiques de gestion de versions : branches, issues, pull requests et revues de code.
- Documenter le dépôt et chaque composant de la base de code (rôle, fonctionnement, utilisation).
- Ajouter des tests, identifier les bogues de la logique backend et les corriger.

## Composants

| Composant            | Fichier(s)                | Rôle                                                        |
|----------------------|---------------------------|-------------------------------------------------------------|
| Frontend – interface | `templates/index.html`    | Affiche la calculatrice et envoie l'expression au serveur   |
| Frontend – style     | `static/style.css`        | Gère l'apparence de l'interface                             |
| Backend – serveur    | `app.py`                  | Exécute le serveur Flask, définit la route et analyse l'expression |
| Backend – logique    | `operators.py`            | Implémente les opérations arithmétiques                     |

## Prérequis

- Un compte GitHub (avec accès au dépôt)
- [Git](https://git-scm.com/)
- [Python](https://www.python.org/) 3.9 ou plus récent
- pip (inclus avec Python)

## Installation

1. **Cloner le dépôt**

   ```bash
   git clone https://github.com/elou14040/TP3_LOG3000.git
   cd TP3_LOG3000
   ```

2. **Créer et activer un environnement virtuel** (recommandé)

   ```bash
   python3 -m venv venv
   source venv/bin/activate        # macOS / Linux
   venv\Scripts\activate           # Windows
   ```

3. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer l'application**

   ```bash
   python app.py
   ```

5. **Ouvrir la calculatrice** dans un navigateur à l'adresse <http://127.0.0.1:5000>.

> **Note macOS :** le port 5000 est souvent occupé par le récepteur AirPlay (la page renvoie
> alors une erreur 403). Lancez plutôt l'application sur un autre port :
>
> ```bash
> flask --app app run --port 5001
> ```
>
> puis ouvrez <http://127.0.0.1:5001>.
